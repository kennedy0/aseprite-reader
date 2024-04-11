from __future__ import annotations
from typing import Optional, TYPE_CHECKING

from PIL import Image

from aseprite_reader import utils
from aseprite_reader.composite import composite

if TYPE_CHECKING:
    from aseprite_reader import AsepriteFile
    from aseprite_reader.chunks import LayerChunk
    from aseprite_reader.chunks import CelChunk
    from aseprite_reader.frame import Frame


def frame_to_image(aseprite_file: AsepriteFile, frame: Frame) -> Image.Image:
    """ Produce an image from frame data. """
    # Initialize frame image
    frame_image = Image.new(mode="RGBA", size=(aseprite_file.header.width, aseprite_file.header.height))

    # Render layers from background to foreground
    for layer in aseprite_file.layers:
        # Only render visible layers with a "child level" of 0 (i.e. have no parents)
        if layer.visible and layer.layer_child_level == 0:
            # Render image for layer
            layer_image = layer_to_image(aseprite_file, frame, layer)

            # An image may not have been created if there was no data in the cel
            if not layer_image:
                continue

            # Get layer opacity
            if aseprite_file.header.layer_opacity_has_valid_value:
                layer_opacity = layer.opacity
            else:
                layer_opacity = 255

            # Composite layer image onto frame image
            frame_image = composite(frame_image, layer_image, layer.blend_mode, layer_opacity)

    return frame_image


def layer_to_image(aseprite_file: AsepriteFile, frame: Frame, layer: LayerChunk) -> Optional[Image.Image]:
    """ Produce an image from layer data. """
    match layer.layer_type:
        case 0:
            return _normal_layer_to_image(aseprite_file, frame, layer)
        case 1:
            return _group_layer_to_image(aseprite_file, frame, layer)
        case 2:
            return _tilemap_layer_to_image(aseprite_file, frame, layer)
        case _:
            raise RuntimeError(f"Invalid layer type: {layer.layer_type}")


def _normal_layer_to_image(aseprite_file: AsepriteFile, frame: Frame, layer: LayerChunk) -> Optional[Image.Image]:
    """ Produce an image from a normal layer. """
    cel = aseprite_file.cel(frame, layer)
    if cel:
        cel_image = cel_to_image(aseprite_file, frame, layer, cel)
        return cel_image


def _group_layer_to_image(aseprite_file: AsepriteFile, frame: Frame, layer: LayerChunk) -> Image.Image:
    """ Produce an image from a group layer. """
    raise NotImplementedError("Group rendering is not implemented.")


def _tilemap_layer_to_image(aseprite_file: AsepriteFile, frame: Frame, layer: LayerChunk) -> Image.Image:
    """ Produce an image from a tilemap layer. """
    raise NotImplementedError("Tilemap rendering is not implemented.")


def cel_to_image(aseprite_file: AsepriteFile, frame: Frame, layer: LayerChunk, cel: CelChunk) -> Image.Image:
    """ Produce an image from cel data. """
    match cel.cel_type:
        case 0:
            return _raw_image_cel_to_image(aseprite_file, frame, layer, cel)
        case 1:
            return _linked_cel_to_image(aseprite_file, frame, layer, cel)
        case 2:
            return _image_cel_to_image(aseprite_file, frame, layer, cel)
        case 3:
            return _tilemap_layer_to_image(aseprite_file, frame, layer)
        case _:
            raise RuntimeError(f"return cel type: {cel.cel_type}")


def _raw_image_cel_to_image(aseprite_file: AsepriteFile, frame: Frame, layer: LayerChunk, cel: CelChunk) -> Image.Image:
    """ Produce an image from a compressed image cel. """
    raise NotImplementedError("Raw image cel rendering is not implemented.")


def _linked_cel_to_image(aseprite_file: AsepriteFile, frame: Frame, layer: LayerChunk, cel: CelChunk) -> Image.Image:
    """ Produce an image from a linked cel. """
    raise NotImplementedError("Linked cel rendering is not implemented.")


def _image_cel_to_image(aseprite_file: AsepriteFile, frame: Frame, layer: LayerChunk, cel: CelChunk) -> Image.Image:
    """ Produce an image from a compressed image cel. """
    # Create new image
    cel_image = Image.new(mode="RGBA", size=(aseprite_file.header.width, aseprite_file.header.height))

    # Decompress image data
    image_data = utils.decompress_image_data(cel.compressed_image_data)
    pixels = utils.image_data_to_pixels(aseprite_file, image_data)

    # Write pixel data from cel to image
    for index, pixel in enumerate(pixels):
        # Convert position in 1D array to 2D grid
        x = index % cel.width
        y = int(index / cel.width)

        # Apply cel position offset
        i = x + cel.x_position
        j = y + cel.y_position

        # Write pixel
        if 0 <= i < cel_image.width and 0 <= j < cel_image.height:
            cel_image.putpixel((i, j), pixel)

    return cel_image


def _tilemap_cel_to_image(aseprite_file: AsepriteFile, frame: Frame, layer: LayerChunk, cel: CelChunk) -> Image.Image:
    """ Produce an image from a tilemap cel. """
    raise NotImplementedError("Tilemap cel rendering is not implemented.")
