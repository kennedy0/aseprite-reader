import os
from typing import IO

from aseprite_reader.chunk import Chunk
from aseprite_reader import utils


class CelExtraChunk(Chunk):
    """ Adds extra information to the latest read cel. """
    def __init__(self, file: IO) -> None:
        self._flags = 0
        self._precise_x_position = 0.0
        self._precise_y_position = 0.0
        self._width_of_cel_in_sprite = 0.0
        self._height_of_cel_in_sprite = 0.0

        super().__init__(file)

    @property
    def flags(self) -> int:
        """ Flags (set to zero)
        1 = Precise bounds are set
        """
        return self._flags

    @property
    def precise_x_position(self) -> float:
        """ Precise X position. """
        return self._precise_x_position

    @property
    def precise_y_position(self) -> float:
        """ Precise Y position. """
        return self._precise_y_position

    @property
    def width_of_cell_in_sprite(self) -> float:
        """ Width of the cel in the sprite (scaled in real-time). """
        return self._width_of_cel_in_sprite

    @property
    def height_of_cell_in_sprite(self) -> float:
        """ Height of the cel in the sprite. """
        return self._height_of_cel_in_sprite

    def _read_file(self, file: IO) -> None:
        super()._read_file(file)
        self._flags = utils.read_dword(file)
        self._precise_x_position = utils.read_fixed(file)
        self._precise_y_position = utils.read_fixed(file)
        self._width_of_cel_in_sprite = utils.read_fixed(file)
        self._height_of_cel_in_sprite = utils.read_fixed(file)
        file.seek(16, os.SEEK_CUR)
