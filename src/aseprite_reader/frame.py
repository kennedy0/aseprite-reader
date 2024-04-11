import os
from typing import IO

from aseprite_reader import utils
from aseprite_reader.chunk import Chunk
from aseprite_reader.chunks import CelChunk


class Frame:
    def __init__(self, file: IO):
        self._offset = 0
        self._size = 0
        self._magic_number = 0
        self._duration = 0
        self._chunk_count_old = 0
        self._chunk_count_new = 0
        self._chunks = []

        self._read_file(file)
        self._go_to_end_of_frame(file)

    @property
    def duration(self) -> int:
        """ Frame duration (in milliseconds) """
        return self._duration

    @property
    def chunk_count(self) -> int:
        """ Number of chunks in this frame.
        If the new chunk field is 0, use the old field.
        """
        if self._chunk_count_new == 0:
            return self._chunk_count_new
        else:
            return self._chunk_count_old

    @property
    def chunks(self) -> list[Chunk]:
        """ A list of chunks in this frame. """
        return self._chunks
    
    @property
    def cels(self) -> list[CelChunk]:
        """ A list of cels in this frame. """
        cels = []
        for chunk in self.chunks:
            if isinstance(chunk, CelChunk):
                cels.append(chunk)

        return cels

    def _go_to_end_of_frame(self, file: IO) -> None:
        """ Move the file position to the end of the frame. """
        file.seek(self._offset + self._size)

    def _read_file(self, file: IO):
        """ Read frame data. """
        self._offset = file.tell()
        self._size = utils.read_dword(file)
        self._magic_number = utils.read_word(file)
        self._chunk_count_old = utils.read_word(file)
        self._duration = utils.read_word(file)
        file.seek(2, os.SEEK_CUR)  # For future (set to zero)
        self._chunk_count_new = utils.read_dword(file)

        # Add each chunk
        for _ in range(self.chunk_count):
            c = Chunk.create_chunk(file)
            self._chunks.append(c)
