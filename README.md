`aseprite_reader` is a Python module for reading and rendering Aseprite files.

## Usage
The `AsepriteFile` class can read and render Aseprite files.

**Example: Render an Aseprite file to a PNG**
```python
from pathlib import Path

from aseprite_reader impor AsepriteFile

src = Path("my_sprite.aseprite")
dst = Path("my_sprite.png")

file = AsepriteFile(src)
file.render(file.frame(1), dst)
```

**Example: Render all frames in an Asprite file as PNGs**
```python
from pathlib import Path

from aseprite_reader impor AsepriteFile

src = Path("my_sprite.aseprite")

file = AsepriteFile(src)
for frame_number, frame in file.iter_frames():
    dst = Path(f"my_sprite.{frame_number:04d}.png")
    file.render(frame, dst)
```

## Development
Create a virtual environment:
```sh
uv venv
```

Install requirements:
```sh
uv sync
```

## A note from Andrew
This is a module that I created and maintain for my own personal projects.
Please keep the following in mind:
- Not all Asprite features are supported.
- Issues are fixed as my time and interest allow.
- Version updates may introduce breaking changes.
