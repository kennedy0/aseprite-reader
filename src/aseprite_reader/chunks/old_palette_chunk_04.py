from aseprite_reader.chunk import Chunk


class OldPaletteChunk04(Chunk):
    """ Ignore this chunk if you find the new palette chunk (0x2019).
    Aseprite v1.1 saves both chunks 0x0004 and 0x2019 just for backward compatibility. """
    pass
