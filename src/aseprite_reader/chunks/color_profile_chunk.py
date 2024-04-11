import os
from typing import Any, IO, Optional

from aseprite_reader.chunk import Chunk
from aseprite_reader import utils


class ColorProfileChunk(Chunk):
    """ Color profile for RGB or grayscale values. """
    def __init__(self, file: IO) -> None:
        self._profile_type = 0
        self._flags = 0
        self._fixed_gamma = 0.0
        self._icc_profile_data_length = None
        self._icc_profile_data = None

        super().__init__(file)

    @property
    def profile_type(self) -> int:
        """ Type.
        0 - no color profile (as in old .aseprite files)
        1 - use sRGB
        2 - use the embedded ICC profile
        """
        return self._profile_type

    @property
    def flags(self) -> int:
        """ Flags.
        1 - use special fixed gamma
        """
        return self._flags

    @property
    def fixed_gamma(self) -> float:
        """ Fixed gamma (1.0 = linear).
        Note: The gamma in sRGB is 2.2 in overall but it doesn't use this fixed gamma,
        because sRGB uses different gamma sections (linear and non-linear).
        If sRGB is specified with a fixed gamma = 1.0, it means that this is Linear sRGB.
        """
        return self._fixed_gamma

    @property
    def icc_profile_data_length(self) -> Optional[int]:
        """ ICC profile data length. """
        return self._icc_profile_data_length

    @property
    def icc_profile_data(self) -> Optional[bytes]:
        """ ICC profile data.
        More info: http://www.color.org/ICC1V42.pdf
        """
        return self._icc_profile_data

    def _read_file(self, file: IO) -> None:
        super()._read_file(file)
        self._profile_type = utils.read_word(file)
        self._flags = utils.read_word(file)
        self._fixed_gamma = utils.read_fixed(file)
        file.seek(8, os.SEEK_CUR)  # Reserved (set to zero)

        # If type = ICC:
        if self.profile_type == 2:
            self._icc_profile_data_length = utils.read_dword(file)
            self._icc_profile_data = file.read(self.icc_profile_data_length)
