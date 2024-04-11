import os
from typing import IO

from aseprite_reader import utils


class Header:
    def __init__(self, file: IO):
        self._file_size = 0
        self._frame_count = 0
        self._width = 0
        self._height = 0
        self._color_depth = 0
        self._flags = 0
        self._speed = 0
        self._transparent_color_index = 0
        self._colors = 0
        self._pixel_width = 0
        self._pixel_height = 0
        self._grid_x = 0
        self._grid_y = 0
        self._grid_width = 0
        self._grid_height = 0

        self._read_file(file)

    @property
    def file_size(self) -> int:
        """ The size of the file """
        return self._file_size

    @property
    def frame_count(self) -> int:
        """ The number of frames in the file. """
        return self._frame_count

    @property
    def width(self) -> int:
        """ Width in pixels. """
        return self._width

    @property
    def height(self) -> int:
        """ Height in pixels. """
        return self._height

    @property
    def color_depth(self):
        # Color depth (bits per pixel)
        #   32 bpp = RGBA
        #   16 bpp = Grayscale
        #   8 bpp = Indexed
        return self._color_depth

    @property
    def flags(self) -> int:
        """ Flags
        1 = Layer opacity has valid value
        """
        return self._flags

    @property
    def layer_opacity_has_valid_value(self) -> bool:
        return utils.flag_is_set(self.flags, 1)

    @property
    def speed(self) -> int:
        """ Speed (milliseconds between frame, like in FLC files)
        DEPRECATED: You should use the frame duration field from each frame header.
        """
        return self._speed

    @property
    def transparent_color_index(self) -> int:
        """ Palette entry (index) which represent transparent color in all non-background layers
        (only for Indexed sprites).
        """
        return self._transparent_color_index

    @property
    def colors(self) -> int:
        """ Number of colors (0 means 256 for old sprites). """
        if self._colors == 0:
            return 256
        else:
            return self._colors

    @property
    def pixel_width(self) -> int:
        """ Pixel width. """
        return self._pixel_width

    @property
    def pixel_height(self) -> int:
        """ Pixel height. """
        return self._pixel_height

    @property
    def pixel_aspect_ratio(self) -> float:
        """ Pixel aspect ratio.
        If pixel width or pixel height field is zero, the pixel ratio is 1:1.
        """
        if self._pixel_width == 0 or self._pixel_height == 0:
            return 1
        else:
            return self._pixel_width / self._pixel_height

    @property
    def grid_x(self) -> int:
        """ X position of the grid. """
        return self._grid_x

    @property
    def grid_y(self) -> int:
        """ Y position of the grid. """
        return self._grid_y

    @property
    def grid_width(self) -> int:
        """ Grid width (zero if there is no grid, grid size is 16x16 on Aseprite by default). """
        return self._grid_width

    @property
    def grid_height(self) -> int:
        """ Grid height. """
        return self._grid_height

    def _read_file(self, file: IO):
        """ Read header data. """
        self._file_size = utils.read_dword(file)
        self._magic_number = utils.read_word(file)
        self._frame_count = utils.read_word(file)
        self._width = utils.read_word(file)
        self._height = utils.read_word(file)
        self._color_depth = utils.read_word(file)
        self._flags = utils.read_dword(file)
        self._speed = utils.read_word(file)
        file.seek(4, os.SEEK_CUR)  # Set be 0
        file.seek(4, os.SEEK_CUR)  # Set be 0
        self._transparent_color_index = utils.read_byte(file)
        file.seek(3, os.SEEK_CUR)  # Ignore these bytes
        self._colors = utils.read_word(file)
        self._pixel_width = utils.read_byte(file)
        self._pixel_height = utils.read_byte(file)
        self._grid_x = utils.read_short(file)
        self._grid_y = utils.read_short(file)
        self._grid_width = utils.read_word(file)
        self._grid_height = utils.read_word(file)
        file.seek(84, os.SEEK_CUR)  # For future (set to zero)
