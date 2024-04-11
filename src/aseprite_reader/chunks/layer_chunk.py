import os
from typing import IO, Optional

from aseprite_reader.chunk import Chunk
from aseprite_reader import utils


class LayerChunk(Chunk):
    """ In the first frame should be a set of layer chunks to determine the entire layers layout. """
    def __init__(self, file: IO) -> None:
        self._flags = 0
        self._layer_type = 0
        self._layer_child_level = 0
        self._default_layer_width = 0
        self._default_layer_height = 0
        self._blend_mode = 0
        self._opacity = 0
        self._layer_name = ""
        self._tileset_index = None

        super().__init__(file)

    def __str__(self) -> str:
        return f"LayerChunk({self.layer_name})"

    def __repr__(self) -> str:
        return str(self)

    @property
    def flags(self) -> int:
        """ Flags.
        1 = Visible
        2 = Editable
        4 = Lock movement
        8 = Background
        16 = Prefer linked cels
        32 = The layer group should be displayed collapsed
        64 = The layer is a reference layer
        """
        return self._flags

    @property
    def visible(self) -> bool:
        """ Layer visibility. """
        return utils.flag_is_set(self.flags, 1)

    @property
    def layer_type(self) -> int:
        """ Layer type.
        0 = Normal (image) layer
        1 = Group
        2 = Tilemap
        """
        return self._layer_type

    @property
    def layer_child_level(self) -> int:
        """ The child level is used to show the relationship of this layer with the last one read, for example:
        Layer name and hierarchy      Child Level
        -----------------------------------------------
        - Background                  0
          `- Layer1                   1
        - Foreground                  0
          |- My set1                  1
          |  `- Layer2                2
          `- Layer3                   1
        """
        return self._layer_child_level

    @property
    def default_layer_width(self) -> int:
        """ Default layer width in pixels (ignored). """
        return self._default_layer_width

    @property
    def default_layer_height(self) -> int:
        """ Default layer height in pixels (ignored). """
        return self._default_layer_height

    @property
    def blend_mode(self) -> int:
        """ Blend mode (always 0 for layer set)
        Normal         = 0
        Multiply       = 1
        Screen         = 2
        Overlay        = 3
        Darken         = 4
        Lighten        = 5
        Color Dodge    = 6
        Color Burn     = 7
        Hard Light     = 8
        Soft Light     = 9
        Difference     = 10
        Exclusion      = 11
        Hue            = 12
        Saturation     = 13
        Color          = 14
        Luminosity     = 15
        Addition       = 16
        Subtract       = 17
        Divide         = 18
        """
        return self._blend_mode

    @property
    def opacity(self) -> int:
        """ Opacity.
        Note: valid only if file header flags field has bit 1 set
        """
        return self._opacity

    @property
    def layer_name(self) -> str:
        """ Layer name. """
        return self._layer_name

    @property
    def tileset_index(self) -> Optional[int]:
        """ Tileset index.
        Only set if layer type = 2.
        """
        return self._tileset_index

    def _read_file(self, file: IO) -> None:
        super()._read_file(file)
        self._flags = utils.read_word(file)
        self._layer_type = utils.read_word(file)
        self._layer_child_level = utils.read_word(file)
        self._default_layer_width = utils.read_word(file)
        self._default_layer_height = utils.read_word(file)
        self._blend_mode = utils.read_word(file)
        self._opacity = utils.read_byte(file)
        file.seek(3, os.SEEK_CUR)  # For future (set to zero)
        self._layer_name = utils.read_string(file)
        if self._layer_type == 2:
            self._tileset_index = utils.read_dword(file)
