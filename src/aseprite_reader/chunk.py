from __future__ import annotations

import os
from typing import IO

from aseprite_reader import utils


class Chunk:
    """ Base chunk class. """
    def __init__(self, file: IO) -> None:
        self._offset = 0
        self._size = 0
        self._chunk_type = 0
        
        self._read_file(file)
        self._go_to_end_of_chunk(file)

    def _read_file(self, file: IO) -> None:
        """ Read the file to populate chunk data.
        This needs to be implemented on each chunk type.
        """
        self._offset = file.tell()
        self._size = utils.read_dword(file)
        self._chunk_type = utils.read_word(file)

    def _go_to_end_of_chunk(self, file: IO) -> None:
        """ Move the file position to the end of the chunk. """
        file.seek(self._offset + self._size)

    @classmethod
    def create_chunk(cls, file: IO) -> Chunk:
        """ Factory method to create a chunk based on chunk type. """
        # Read the chunk type from the file, then rewind the file position back to the beginning of the chunk
        file.seek(4, os.SEEK_CUR)  # Chunk size
        chunk_type = utils.read_word(file)
        file.seek(-6, os.SEEK_CUR)

        match chunk_type:
            case 0x0004:
                from aseprite_reader.chunks import OldPaletteChunk04
                return OldPaletteChunk04(file)
            case 0x0011:
                from aseprite_reader.chunks import OldPaletteChunk11
                return OldPaletteChunk11(file)
            case 0x2004:
                from aseprite_reader.chunks import LayerChunk
                return LayerChunk(file)
            case 0x2005:
                from aseprite_reader.chunks import CelChunk
                return CelChunk(file)
            case 0x2006:
                from aseprite_reader.chunks import CelExtraChunk
                return CelExtraChunk(file)
            case 0x2007:
                from aseprite_reader.chunks import ColorProfileChunk
                return ColorProfileChunk(file)
            case 0x2008:
                from aseprite_reader.chunks import ExternalFilesChunk
                return ExternalFilesChunk(file)
            case 0x2016:
                from aseprite_reader.chunks import MaskChunk
                return MaskChunk(file)
            case 0x2017:
                from aseprite_reader.chunks import PathChunk
                return PathChunk(file)
            case 0x2018:
                from aseprite_reader.chunks import TagsChunk
                return TagsChunk(file)
            case 0x2019:
                from aseprite_reader.chunks import PaletteChunk
                return PaletteChunk(file)
            case 0x2020:
                from aseprite_reader.chunks import UserDataChunk
                return UserDataChunk(file)
            case 0x2022:
                from aseprite_reader.chunks import SliceChunk
                return SliceChunk(file)
            case 0x2023:
                from aseprite_reader.chunks import TilesetChunk
                return TilesetChunk(file)
            case _:
                raise Exception(f"Invalid chunk type: {hex(chunk_type)}")
