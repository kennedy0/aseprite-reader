from typing import IO, Optional

from aseprite_reader import utils


class PaletteColor:
    def __init__(self, file: IO):
        self._flags = 0
        self._r = 0
        self._g = 0
        self._b = 0
        self._a = 0
        self._name = None

        self._read_file(file)

    def __str__(self) -> str:
        return f"PaletteColor({self.name})"

    def __repr__(self) -> str:
        return str(self)

    @property
    def flags(self) -> int:
        """ Entry flags:
        1 = Has name
        """
        return self._flags

    @property
    def r(self) -> int:
        """ Red (0-255). """
        return self._r

    @property
    def g(self) -> int:
        """ Green (0-255). """
        return self._g

    @property
    def b(self) -> int:
        """ Blue (0-255). """
        return self._b

    @property
    def a(self) -> int:
        """ Alpha (0-255). """
        return self._a

    @property
    def name(self) -> Optional[str]:
        return self._name

    def _read_file(self, file: IO) -> None:
        self._flags = utils.read_word(file)
        self._r = utils.read_byte(file)
        self._g = utils.read_byte(file)
        self._b = utils.read_byte(file)
        self._a = utils.read_byte(file)

        if utils.flag_is_set(self.flags, 1):
            self._name = utils.read_string(file)
