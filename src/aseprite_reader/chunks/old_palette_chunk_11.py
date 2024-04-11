from aseprite_reader.chunk import Chunk


class OldPaletteChunk11(Chunk):
    """ Ignore this chunk if you find the new palette chunk (0x2019). """
    pass
