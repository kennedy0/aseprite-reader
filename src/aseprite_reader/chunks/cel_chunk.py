import os
from typing import Any, IO, Optional

from aseprite_reader.chunk import Chunk
from aseprite_reader import utils


class CelChunk(Chunk):
    """ This chunk determine where to put a cel in the specified layer/frame. """
    def __init__(self, file: IO) -> None:
        self._layer_index = 0
        self._x_position = 0
        self._y_position = 0
        self._opacity_level = 0
        self._cel_type = 0
        self._width = None
        self._height = None
        self._raw_pixel_data = None
        self._linked_frame_position = None
        self._compressed_image_data = None
        self._width_tiles = None
        self._height_tiles = None
        self._bits_per_tile = None
        self._bitmask_tile_id = None
        self._bitmask_x_flip = None
        self._bitmask_y_flip = None
        self._bitmask_90cw_rotation = None
        self._compressed_tile_data = None

        super().__init__(file)

    @property
    def layer_index(self) -> int:
        """ Layer index.
        The layer index is a number to identify any layer in the sprite, for example:
        Layer name and hierarchy      Layer index
        -----------------------------------------------
        - Background                  0
          `- Layer1                   1
        - Foreground                  2
          |- My set1                  3
          |  `- Layer2                4
          `- Layer3                   5
        """
        return self._layer_index

    @property
    def x_position(self) -> int:
        """ X position. """
        return self._x_position

    @property
    def y_position(self) -> int:
        """ Y position. """
        return self._y_position

    @property
    def opacity_level(self) -> int:
        """ Opacity level. """
        return self._opacity_level

    @property
    def cel_type(self) -> int:
        """ Cel type.
        0 - Raw Image Data (unused, compressed image is preferred)
        1 - Linked Cel
        2 - Compressed Image
        3 - Compressed Tilemap
        """
        return self._cel_type

    @property
    def width(self) -> Optional[int]:
        """ Width in pixels. """
        return self._width

    @property
    def height(self) -> Optional[int]:
        """ Height in pixels. """
        return self._height

    @property
    def raw_pixel_data(self) -> Optional[list[Any]]:
        """ Raw pixel data: row by row from top to bottom, for each scanline read pixels from left to right. """
        return self._raw_pixel_data

    @property
    def linked_frame_position(self) -> Optional[int]:
        """ Frame position to link with. """
        return self._linked_frame_position

    @property
    def compressed_image_data(self) -> Optional[bytes]:
        """ 'Raw Cel' data compressed with ZLIB method. """
        return self._compressed_image_data

    @property
    def width_tiles(self) -> Optional[int]:
        """ Width in number of tiles. """
        return self._width_tiles

    @property
    def height_tiles(self) -> Optional[int]:
        """ Height in number of tiles. """
        return self._height_tiles

    @property
    def bits_per_tile(self) -> Optional[int]:
        """ Bits per tile (at the moment it's always 32-bit per tile). """
        return self._bits_per_tile

    @property
    def bitmask_tile_id(self) -> Optional[int]:
        """ Bitmask for tile ID (e.g. 0x1fffffff for 32-bit tiles). """
        return self._bitmask_tile_id

    @property
    def bitmask_x_flip(self) -> Optional[int]:
        """ Bitmask for X flip. """
        return self._bitmask_x_flip

    @property
    def bitmask_y_flip(self) -> Optional[int]:
        """ Bitmask for Y flip. """
        return self._bitmask_y_flip

    @property
    def bitmask_90cw_rotation(self) -> Optional[int]:
        """ Bitmask for 90CW rotation. """
        return self._bitmask_90cw_rotation

    @property
    def compressed_tile_data(self) -> Optional[bytes]:
        """ Row by row, from top to bottom tile by tile compressed with ZLIB method. """
        return self._compressed_tile_data

    def _read_file(self, file: IO) -> None:
        super()._read_file(file)
        self._layer_index = utils.read_word(file)
        self._x_position = utils.read_short(file)
        self._y_position = utils.read_short(file)
        self._opacity_level = utils.read_byte(file)
        self._cel_type = utils.read_word(file)
        file.seek(7, os.SEEK_CUR)  # For future (set to zero)

        # For cel type 0 (Raw Image Data)
        if self.cel_type == 0:
            self._width = utils.read_word(file)
            self._height = utils.read_word(file)

            # Read rest of the bytes in the chunk as raw pixel data
            bytes_to_read = self._offset + self._size - file.tell()
            self._raw_pixel_data = file.read(bytes_to_read)

        # For cel type 1 (Linked Cel)
        if self.cel_type == 1:
            self._linked_frame_position = utils.read_word(file)

        # For cel type 2 (Compressed Image)
        if self.cel_type == 2:
            self._width = utils.read_word(file)
            self._height = utils.read_word(file)

            # Read rest of the bytes in the chunk as compressed image data
            bytes_to_read = self._offset + self._size - file.tell()
            self._compressed_image_data = file.read(bytes_to_read)

        # For cel type 3 (Compressed Tilemap)
        if self.cel_type == 3:
            self._width_tiles = utils.read_word(file)
            self._height_tiles = utils.read_word(file)
            self._bits_per_tile = utils.read_word(file)
            self._bitmask_tile_id = utils.read_dword(file)
            self._bitmask_x_flip = utils.read_dword(file)
            self._bitmask_y_flip = utils.read_dword(file)
            self._bitmask_90cw_rotation = utils.read_dword(file)
            file.seek(10, os.SEEK_CUR)  # Reserved

            # Read rest of the bytes in the chunk as compressed tile data
            bytes_to_read = self._offset + self._size - file.tell()
            self._compressed_tile_data = file.read(bytes_to_read)
