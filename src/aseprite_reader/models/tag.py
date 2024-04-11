import os
from typing import IO

from aseprite_reader import utils


class Tag:
    def __init__(self, file: IO):
        self._from_frame = 0
        self._to_frame = 0
        self._loop_animation_direction = 0
        self._repeat = 0
        self._color = (0, 0, 0)
        self._name = ""

        self._read_file(file)

    def __str__(self) -> str:
        return f"Tag({self.name})"

    def __repr__(self) -> str:
        return str(self)

    @property
    def from_frame(self) -> int:
        """ From frame. """
        return self._from_frame

    @property
    def to_frame(self) -> int:
        """ To frame. """
        return self._to_frame

    @property
    def loop_animation_direction(self) -> int:
        """ Loop animation direction.
        0 = Forward
        1 = Reverse
        2 = Ping-pong
        3 = Ping-pong Reverse
        """
        return self._loop_animation_direction

    @property
    def repeat(self) -> int:
        """ Repeat N times. Play this animation section N times:
        0 = Doesn't specify (plays infinite in UI, once on export, for ping-pong it plays once in each direction)
        1 = Plays once (for ping-pong, it plays just in one direction)
        2 = Plays twice (for ping-pong, it plays once in one direction, and once in reverse)
        n = Plays N times
        """
        return self._repeat

    @property
    def color(self) -> tuple[int, int, int]:
        """ RGB values of the tag color.
        Deprecated, used only for backward compatibility with Aseprite v1.2.x.
        The color of the tag is the one in the user data field following the tags chunk.
        """
        return self._color

    @property
    def name(self) -> str:
        """ Tag name. """
        return self._name

    def _read_file(self, file: IO) -> None:
        self._from_frame = utils.read_word(file)
        self._to_frame = utils.read_word(file)
        self._loop_animation_direction = utils.read_byte(file)
        self._repeat = utils.read_word(file)
        file.seek(6, os.SEEK_CUR)  # For future (set to zero)
        self._color = utils.read_bytes(3, file)
        file.seek(1, os.SEEK_CUR)  # Extra byte (zero)
        self._name = utils.read_string(file)
