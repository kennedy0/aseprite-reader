import os
from typing import IO

from aseprite_reader import utils


class ExternalFile:
    def __init__(self, file: IO):
        self._entry_id = 0
        self._file_name = ""

        self._read_file(file)

    def __str__(self) -> str:
        return f"ExternalFile({self.file_name})"

    def __repr__(self) -> str:
        return str(self)

    @property
    def entry_id(self) -> int:
        """ Entry ID (this ID is referenced by tilesets or palettes). """
        return self._entry_id

    @property
    def file_name(self) -> str:
        """ External file name. """
        return self._file_name

    def _read_file(self, file: IO) -> None:
        self._entry_id = utils.read_dword(file)
        file.seek(8, os.SEEK_CUR)  # Reserved (set to zero)
        self._file_name = utils.read_string(file)
