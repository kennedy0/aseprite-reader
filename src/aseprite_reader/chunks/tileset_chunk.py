import os
from typing import Any, IO, Optional

from aseprite_reader.chunk import Chunk
from aseprite_reader import utils


class TilesetChunk(Chunk):
    def __init__(self, file: IO) -> None:
        self._tileset_id = 0
        self._flags = 0
        self._tile_count = 0
        self._tile_width = 0
        self._tile_height = 0
        self._base_index = 0
        self._name: str = ""
        self._external_file_id = None
        self._tileset_id_in_external_file = None
        self._compressed_data_length = None
        self._compressed_tileset_image = None

        super().__init__(file)

    @property
    def tileset_id(self) -> int:
        """ Tileset ID. """
        return self._tileset_id

    @property
    def flags(self) -> int:
        """ Tileset flags.
        1 - Include link to external file
        2 - Include tiles inside this file
        4 - Tilemaps using this tileset use tile ID=0 as empty tile (this is the new format).
            In rare cases this bit is off, and the empty tile will be equal to 0xffffffff
            (used in internal versions of Aseprite).
        """
        return self._flags

    @property
    def tile_count(self) -> int:
        """ Number of tiles. """
        return self._tile_count

    @property
    def tile_width(self) -> int:
        """ Tile Width. """
        return self._tile_width

    @property
    def tile_height(self) -> int:
        """ Tile Height. """
        return self._tile_height

    @property
    def base_index(self) -> int:
        """ Base Index: Number to show in the screen from the tile with index 1 and so on
        (by default this is field is 1, so the data that is displayed is equivalent to the data in memory).
        But it can be 0 to display zero-based indexing
        (this field isn't used for the representation of the data in the file, it's just for UI purposes).
        """
        return self._base_index

    @property
    def name(self) -> str:
        """ Name of the tileset. """
        return self._name

    @property
    def external_file_id(self) -> Optional[int]:
        """ ID of the external file.
        This ID is one entry of the External Files Chunk.
        """
        return self._external_file_id

    @property
    def tileset_id_in_external_file(self) -> Optional[int]:
        """ Tileset ID in external file. """
        return self._tileset_id_in_external_file

    @property
    def compressed_data_length(self) -> Optional[int]:
        """ Compressed data length. """
        return self._compressed_data_length

    @property
    def compressed_tileset_image(self) -> Optional[bytes]:
        """ Compressed Tileset image:
            (Tile Width) x (Tile Height X Number of Tiles)
        """
        return self._compressed_tileset_image

    def _read_file(self, file: IO) -> None:
        super()._read_file(file)
        self._tileset_id = utils.read_dword(file)
        self._flags = utils.read_dword(file)
        self._tile_count = utils.read_dword(file)
        self._tile_width = utils.read_word(file)
        self._tile_height = utils.read_word(file)
        self._base_index = utils.read_short(file)
        file.seek(14, os.SEEK_CUR)  # Reserved
        self._name = utils.read_string(file)

        # If flag 1 is set
        if utils.flag_is_set(self.flags, 1):
            self._external_file_id = utils.read_dword(file)
            self._tileset_id_in_external_file = utils.read_dword(file)

        # If flag 2 is set
        if utils.flag_is_set(self.flags, 2):
            self._compressed_data_length = utils.read_dword(file)
            self._compressed_tileset_image = file.read(self.compressed_data_length)
