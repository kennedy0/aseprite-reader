from typing import IO, Optional

from aseprite_reader.chunk import Chunk
from aseprite_reader import utils


class UserDataChunk(Chunk):
    """ Insert this user data in the last read chunk.
    E.g. If we've read a layer, this user data belongs to that layer, if we've read a cel, it belongs to that cel, etc.
    There are some special cases:
    After a Tags chunk, there will be several user data fields, one for each tag, you should associate the user data in
        the same order as the tags are in the Tags chunk.
    In version 1.3 a sprite has associated user data, to consider this case there is an User Data Chunk at the first
        frame after the Palette Chunk
    """
    def __init__(self, file: IO) -> None:
        self._flags: int = 0
        self._text = None
        self._red = None
        self._green = None
        self._blue = None
        self._alpha = None

        super().__init__(file)

    @property
    def flags(self) -> int:
        """ Flags.
        1 = Has text
        2 = Has color
        """
        return self._flags

    @property
    def text(self) -> Optional[str]:
        """ Text """
        return self._text

    @property
    def red(self) -> Optional[int]:
        """ Color red (0-255). """
        return self._red

    @property
    def green(self) -> Optional[int]:
        """ Color green (0-255). """
        return self._green

    @property
    def blue(self) -> Optional[int]:
        """ Color blue (0-255). """
        return self._blue

    @property
    def alpha(self) -> Optional[int]:
        """ Color alpha (0-255). """
        return self._alpha

    def _read_file(self, file: IO) -> None:
        super()._read_file(file)
        self._flags = utils.read_dword(file)

        # If flags have bit 1
        if utils.flag_is_set(self.flags, 1):
            self._text = utils.read_string(file)

        # If flags have bit 2
        if utils.flag_is_set(self._flags, 2):
            self._red = utils.read_byte(file)
            self._green = utils.read_byte(file)
            self._blue = utils.read_byte(file)
            self._alpha = utils.read_byte(file)
