from pathlib import Path
from typing import Iterator, Optional

from aseprite_reader import render
from aseprite_reader import utils
from aseprite_reader.chunks import CelChunk, LayerChunk, TagsChunk
from aseprite_reader.frame import Frame
from aseprite_reader.header import Header
from aseprite_reader.models import Tag


ASEPRITE_MAGIC_NUMBER = 0xa5e0


class AsepriteFile:
    def __init__(self, file_path: str | Path) -> None:
        if isinstance(file_path, str):
            file_path = Path(file_path)

        self._file_path = file_path
        self._header = None
        self._frames = []

        self._validate()
        self._read_file()

    def __str__(self) -> str:
        return f"AsepriteFile({self._file_path.as_posix()})"

    def __repr__(self) -> str:
        return str(self)

    @property
    def file_path(self) -> Path:
        """ The path to the Aseprite file. """
        return self._file_path

    @property
    def header(self) -> Header:
        """ The file header. """
        return self._header

    @property
    def frames(self) -> list[Frame]:
        """ A list of frames in the file. """
        return self._frames

    @property
    def tags(self) -> list[Tag]:
        """ A list of tags in the file. """
        tags = []
        first_frame = self.frame(1)
        for chunk in first_frame.chunks:
            if isinstance(chunk, TagsChunk):
                tags = chunk.tags

        return tags

    @property
    def layers(self) -> list[LayerChunk]:
        """ A list of layers in the file. """
        layers = []
        first_frame = self.frame(1)
        for chunk in first_frame.chunks:
            if isinstance(chunk, LayerChunk):
                layers.append(chunk)

        return layers

    def _validate(self) -> None:
        """ Make sure this is a valid Aseprite file. """
        with self.file_path.open('rb') as f:
            f.seek(4)
            if utils.read_word(f) != ASEPRITE_MAGIC_NUMBER:
                raise Exception(f"{self.file_path.as_posix()} is not a valid Aseprite file")

    def _read_file(self) -> None:
        """ Read header and frame data. """
        with self.file_path.open('rb') as f:
            self._header = Header(f)
            for _ in range(self.header.frame_count):
                self._frames.append(Frame(f))

    def frame(self, frame_number: int) -> Frame:
        """ Get a frame from its frame number. """
        try:
            return self.frames[frame_number-1]
        except IndexError:
            raise IndexError(f"Frame {frame_number} does not exist (frame range is 1-{len(self.frames)}).")

    def cel(self, frame: Frame, layer: LayerChunk) -> Optional[CelChunk]:
        """ Get a layer's cel on a specific frame. """
        layer_index = self.layers.index(layer)
        for cel in frame.cels:
            if cel.layer_index == layer_index:
                return cel

    def frame_tags(self, frame_number: int) -> list[Tag]:
        """ Get a list of tags on a frame number. """
        tags = []
        for tag in self.tags:
            if tag.from_frame <= frame_number - 1 <= tag.to_frame:
                if tag not in tags:
                    tags.append(tag)

        return tags

    def iter_frames(self) -> Iterator[tuple[int, Frame]]:
        """ Iterate over frames in the file.
        A tuple of (frame_number, Frame) is returned.
        """
        start = 1
        end = len(self.frames)

        for f in range(start, end + 1):
            frame = self.frame(f)
            frame_number = f - start + 1
            yield frame_number, frame

    def render(self, frame: Frame, output_file: Path) -> None:
        """ Render a frame as a PNG image. """
        # Make sure 'output_file' has a .png extension
        if not output_file.suffix == ".png":
            raise RuntimeError(f"Output file {output_file.as_posix()} must have a '.png' extension.")

        # Make sure output file doesn't already exist
        if output_file.exists():
            raise FileExistsError(f"Can't overwrite existing file: {output_file.as_posix()}")

        image = render.frame_to_image(self, frame)
        image.save(output_file)
