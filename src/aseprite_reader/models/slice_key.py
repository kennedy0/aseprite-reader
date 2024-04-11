from typing import IO, Optional

from aseprite_reader import utils


class SliceKey:
    def __init__(self, file: IO, flags: int):
        self._frame_number = 0
        self._x_origin = 0
        self._y_origin = 0
        self._slice_width = 0
        self._slice_height = 0
        self._center_x = None
        self._center_y = None
        self._center_w = None
        self._center_h = None
        self._pivot_x = None
        self._pivot_y = None

        self._read_file(file, flags)

    @property
    def frame_number(self) -> int:
        """ Frame number (this slice is valid form this frame to the end of the animation). """
        return self._frame_number

    @property
    def x_origin(self) -> int:
        """ Slice X origin coordinate in the sprite. """
        return self._x_origin

    @property
    def y_origin(self) -> int:
        """ Slice Y origin coordinate in the sprite. """
        return self._y_origin

    @property
    def slice_width(self) -> int:
        """ Slice width (can be 0 if this slice hidden in the animation from the given frame). """
        return self._slice_width

    @property
    def slice_height(self) -> int:
        """ Slice height. """
        return self._slice_height

    @property
    def center_x(self) -> Optional[int]:
        """ Center X position (relative to slice bounds). """
        return self._center_x

    @property
    def center_y(self) -> Optional[int]:
        """ Center Y position. """
        return self._center_y

    @property
    def center_w(self) -> Optional[int]:
        """ Center width. """
        return self._center_w

    @property
    def center_h(self) -> Optional[int]:
        """ Center height. """
        return self._center_h

    @property
    def pivot_x(self) -> Optional[int]:
        """ Pivot X position (relative to the slice origin). """
        return self._pivot_x

    @property
    def pivot_y(self) -> Optional[int]:
        """ Pivot Y position (relative to the slice origin). """
        return self._pivot_y

    def _read_file(self, file: IO, flags: int) -> None:
        self._frame_number = utils.read_dword(file)
        self._x_origin = utils.read_long(file)
        self._y_origin = utils.read_long(file)
        self._slice_width = utils.read_dword(file)
        self._slice_height = utils.read_dword(file)

        # + If flags have bit 1
        if utils.flag_is_set(flags, 1):
            self._center_x = utils.read_long(file)
            self._center_y = utils.read_long(file)
            self._center_w = utils.read_dword(file)
            self._center_h = utils.read_dword(file)

        # + If flags have bit 2
        if utils.flag_is_set(flags, 2):
            self._pivot_x = utils.read_long(file)
            self._pivot_y = utils.read_long(file)
