import os
from typing import IO

from aseprite_reader import utils
from aseprite_reader.chunk import Chunk
from aseprite_reader.models import PaletteColor


class PaletteChunk(Chunk):
    def __init__(self, file: IO) -> None:
        self._palette_size = 0
        self._first_index_to_change = 0
        self._last_index_to_change = 0
        self._palette_colors = []

        super().__init__(file)

    @property
    def palette_size(self) -> int:
        """ New palette size (total number of entries). """
        return self._palette_size

    @property
    def first_index_to_change(self) -> int:
        """ First color index to change. """
        return self._first_index_to_change

    @property
    def last_index_to_change(self) -> int:
        """ Last color index to change. """
        return self._last_index_to_change

    @property
    def palette_colors(self) -> list[PaletteColor]:
        """ A list of colors in this palette. """
        return self._palette_colors

    def _read_file(self, file: IO) -> None:
        super()._read_file(file)
        self._palette_size = utils.read_dword(file)
        self._first_index_to_change = utils.read_dword(file)
        self._last_index_to_change = utils.read_dword(file)
        file.seek(8, os.SEEK_CUR)  # For future (set to zero)

        # Add each palette color
        for _ in range(self._palette_size):
            palette_color = PaletteColor(file)
            self._palette_colors.append(palette_color)
