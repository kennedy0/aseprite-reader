from typing import IO

from aseprite_reader import utils
from aseprite_reader.chunk import Chunk
from aseprite_reader.models import SliceKey


class SliceChunk(Chunk):
    def __init__(self, file: IO) -> None:
        self._slice_key_count = 0
        self._flags = 0
        self._name = ""
        self._slice_keys = []

        super().__init__(file)

    @property
    def slice_key_count(self) -> int:
        """ Number of slice keys. """
        return self._slice_key_count

    @property
    def flags(self) -> int:
        """ Flags.
        1 = It's a 9-patches slice
        2 = Has pivot information
        """
        return self._flags

    @property
    def name(self) -> str:
        """ Name """
        return self._name

    @property
    def slice_keys(self) -> list[SliceKey]:
        return self._slice_keys

    def _read_file(self, file: IO) -> None:
        super()._read_file(file)
        self._slice_key_count = utils.read_dword(file)
        self._flags = utils.read_dword(file)
        utils.read_dword(file)  # Reserved
        self._name = utils.read_string(file)

        # Add each slice key
        for _ in range(self.slice_key_count):
            slice_key = SliceKey(file, self.flags)
            self._slice_keys.append(slice_key)
