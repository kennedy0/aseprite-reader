from __future__ import annotations
import struct
import zlib
from typing import IO, TYPE_CHECKING

from aseprite_reader.chunks import PaletteChunk

if TYPE_CHECKING:
    from aseprite_reader import AsepriteFile


Color = tuple[int, int, int, int]


def read_byte(file: IO) -> int:
    """ Read a BYTE.
    An 8-bit unsigned integer value.
    """
    return struct.unpack('<B', file.read(1))[0]


def read_bytes(num_bytes: int, file: IO) -> tuple[int]:
    """ Read multiple BYTES. """
    return struct.unpack(f'<{num_bytes}B', file.read(num_bytes))  # noqa


def read_word(file: IO) -> int:
    """ Read a WORD.
    A 16-bit unsigned integer value.
    """
    return struct.unpack('<H', file.read(2))[0]


def read_short(file: IO) -> int:
    """ Read a SHORT.
    A 16-bit signed integer value.
    """
    return struct.unpack('<h', file.read(2))[0]


def read_dword(file: IO) -> int:
    """ Read a DWORD.
    A 32-bit unsigned integer value.
    """
    return struct.unpack('<I', file.read(4))[0]


def read_long(file: IO) -> int:
    """ Read a LONG.
    A 32-bit signed integer value.
    """
    return struct.unpack('<l', file.read(4))[0]


def read_fixed(file: IO) -> float:
    """ Read a FIXED.
    A 32-bit fixed point (16.16) value.
    """
    return struct.unpack('<I', file.read(4))[0] / 65536.0


def read_string(file: IO) -> str:
    """ Read a STRING.
    WORD: string length (number of bytes).
    BYTE[length]: characters (in UTF-8) The '\0' character is not included..
    """
    length = read_word(file)
    return file.read(length).decode("utf-8")


def decompress_image_data(compressed_data: bytes) -> tuple[int]:
    """ Decompress image data that is ZLIB compressed. """
    decompressed_data = []
    for b in zlib.decompress(compressed_data):
        decompressed_data.append(b)
    return tuple(decompressed_data)


def image_data_to_pixels(aseprite_file: AsepriteFile, decompressed_data: tuple[int]) -> tuple[Color]:
    """ Convert decompressed image data into an array of pixels. """
    match aseprite_file.header.color_depth:
        case 32:
            return _image_data_to_pixels_rgba(decompressed_data)
        case 16:
            return _image_data_to_pixels_grayscale(decompressed_data)
        case 8:
            return _image_data_to_pixels_indexed(aseprite_file, decompressed_data)
        case _:
            raise RuntimeError(f"Invalid color depth: {aseprite_file.header.color_depth}")


def _image_data_to_pixels_rgba(decompressed_data: tuple[int]) -> tuple[Color]:
    """ Convert rgba image data to pixels. """
    pixels = []

    for i in range(0, len(decompressed_data), 4):
        r, g, b, a = tuple(decompressed_data[i:i + 4])
        pixels.append((r, g, b, a))

    return tuple(pixels)  # noqa


def _image_data_to_pixels_grayscale(decompressed_data: tuple[int]) -> tuple[Color]:
    """ Convert grayscale image data to pixels. """
    pixels = []

    for i in range(0, len(decompressed_data), 2):
        v, a = decompressed_data[i:i + 2]
        pixels.append((v, v, v, a))

    return tuple(pixels)  # noqa


def _image_data_to_pixels_indexed(aseprite_file: AsepriteFile, decompressed_data: tuple[int]) -> tuple[Color]:
    """ Convert indexed image data to pixels. """
    pixels = []

    # Get palette colors
    palette = None
    first_frame = aseprite_file.frame(1)
    for chunk in first_frame.chunks:
        if isinstance(chunk, PaletteChunk):
            palette = chunk
            break

    # Make sure that we found a palette
    if not palette:
        raise RuntimeError("Error reading indexed colors: could not find palette chunk.")

    for i in decompressed_data:
        if i == aseprite_file.header.transparent_color_index:
            pixels.append((0, 0, 0, 0))
        else:
            color = palette.palette_colors[i]
            pixels.append((color.r, color.g, color.b, color.a))

    return tuple(pixels)  # noqa


def flag_is_set(flags: int, flag: int) -> bool:
    """ Check if a flag is set. """
    return flags & flag != 0
