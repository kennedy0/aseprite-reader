import os
from typing import IO

from aseprite_reader import utils
from aseprite_reader.chunk import Chunk
from aseprite_reader.models import Tag


class TagsChunk(Chunk):
    """ Stores the tags in the file. """
    def __init__(self, file: IO) -> None:
        self._tag_count = 0
        self._tags = []

        super().__init__(file)

    @property
    def tag_count(self) -> int:
        """ Number of tags. """
        return self._tag_count

    @property
    def tags(self) -> list[Tag]:
        """ A list of tags in the file. """
        return self._tags

    def _read_file(self, file: IO) -> None:
        super()._read_file(file)
        self._tag_count = utils.read_word(file)
        file.seek(8, os.SEEK_CUR)  # For future (set to zero)

        # Add each tag
        for _ in range(self._tag_count):
            tag = Tag(file)
            self._tags.append(tag)
