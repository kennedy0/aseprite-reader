import os
from typing import IO

from aseprite_reader import utils
from aseprite_reader.chunk import Chunk
from aseprite_reader.models import ExternalFile


class ExternalFilesChunk(Chunk):
    """ A list of external files linked with this file. It might be used to reference external palettes or tilesets. """
    def __init__(self, file: IO) -> None:
        self._entry_count = 0
        self._external_files = []

        super().__init__(file)

    @property
    def entry_count(self) -> int:
        """ Number of entries. """
        return self._entry_count

    def _read_file(self, file: IO) -> None:
        super()._read_file(file)
        self._entry_count = utils.read_dword(file)
        file.seek(8, os.SEEK_CUR)  # Reserved (set to zero)

        # Add each external file
        for _ in range(self._entry_count):
            external_file = ExternalFile(file)
            self._external_files.append(external_file)
