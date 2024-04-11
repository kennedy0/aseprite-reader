from PIL import Image


def composite(bg: Image.Image, fg: Image.Image, blend_mode: int = 0, fg_opacity: int = 255) -> Image.Image:
    """ Composite a background image onto a foreground image. """
    # Apply fg opacity
    if fg_opacity < 255:
        _apply_opacity(fg, fg_opacity)

    # Blend images
    match blend_mode:
        case 0:
            image = _blend_normal(bg, fg)
        case 1:
            image = _blend_multiply(bg, fg)
        case 2:
            image = _blend_screen(bg, fg)
        case 3:
            image = _blend_overlay(bg, fg)
        case 4:
            image = _blend_darken(bg, fg)
        case 5:
            image = _blend_lighten(bg, fg)
        case 6:
            image = _blend_color_dodge(bg, fg)
        case 7:
            image = _blend_color_burn(bg, fg)
        case 8:
            image = _blend_hard_light(bg, fg)
        case 9:
            image = _blend_soft_light(bg, fg)
        case 10:
            image = _blend_difference(bg, fg)
        case 11:
            image = _blend_exclusion(bg, fg)
        case 12:
            image = _blend_hue(bg, fg)
        case 13:
            image = _blend_saturation(bg, fg)
        case 14:
            image = _blend_color(bg, fg)
        case 15:
            image = _blend_luminosity(bg, fg)
        case 16:
            image = _blend_addition(bg, fg)
        case 17:
            image = _blend_subtract(bg, fg)
        case 18:
            image = _blend_divide(bg, fg)
        case _:
            raise RuntimeError(f"Unsupported blend mode: {blend_mode}")

    return image


def _apply_opacity(image: Image.Image, opacity: int) -> None:
    """ Apply an opacity value (0-255) to an image. """
    # Don't need to change the image if there is full opacity
    if opacity == 255:
        return

    # Scale opacity to 0-1 range
    f_opacity = float(opacity) / 255.0

    # Create a function to scale the pixels in the alpha channel by the opacity value
    def __mult_alpha(pixel: int):
        return int(pixel * f_opacity)

    # Multiply alpha channel by opacity value
    alpha = image.getchannel("A")
    alpha = alpha.point(__mult_alpha)

    # Add new alpha channel to image
    image.putalpha(alpha)


def _blend_normal(bg: Image.Image, fg: Image.Image) -> Image.Image:
    """ Normal blend mode. """
    return Image.alpha_composite(bg, fg)


def _blend_multiply(bg: Image.Image, fg: Image.Image) -> Image.Image:
    """ Multiply blend mode. """
    raise NotImplementedError("Multiply blend mode is not implemented.")


def _blend_screen(bg: Image.Image, fg: Image.Image) -> Image.Image:
    """ Screen blend mode. """
    raise NotImplementedError("Screen blend mode is not implemented.")


def _blend_overlay(bg: Image.Image, fg: Image.Image) -> Image.Image:
    """ Overlay blend mode. """
    raise NotImplementedError("Overlay blend mode is not implemented.")


def _blend_darken(bg: Image.Image, fg: Image.Image) -> Image.Image:
    """ Darken blend mode. """
    raise NotImplementedError("Darken blend mode is not implemented.")


def _blend_lighten(bg: Image.Image, fg: Image.Image) -> Image.Image:
    """ Lighten blend mode. """
    raise NotImplementedError("Lighten blend mode is not implemented.")


def _blend_color_dodge(bg: Image.Image, fg: Image.Image) -> Image.Image:
    """ Color dodge blend mode. """
    raise NotImplementedError("Color dodge blend mode is not implemented.")


def _blend_color_burn(bg: Image.Image, fg: Image.Image) -> Image.Image:
    """ Color burn blend mode. """
    raise NotImplementedError("Color burn blend mode is not implemented.")


def _blend_hard_light(bg: Image.Image, fg: Image.Image) -> Image.Image:
    """ Hard light blend mode. """
    raise NotImplementedError("Hard light blend mode is not implemented.")


def _blend_soft_light(bg: Image.Image, fg: Image.Image) -> Image.Image:
    """ Soft light blend mode. """
    raise NotImplementedError("Soft light blend mode is not implemented.")


def _blend_difference(bg: Image.Image, fg: Image.Image) -> Image.Image:
    """ Difference blend mode. """
    raise NotImplementedError("Difference blend mode is not implemented.")


def _blend_exclusion(bg: Image.Image, fg: Image.Image) -> Image.Image:
    """ Exclusion blend mode. """
    raise NotImplementedError("Exclusion blend mode is not implemented.")


def _blend_hue(bg: Image.Image, fg: Image.Image) -> Image.Image:
    """ Hue blend mode. """
    raise NotImplementedError("Hue blend mode is not implemented.")


def _blend_saturation(bg: Image.Image, fg: Image.Image) -> Image.Image:
    """ Saturation blend mode. """
    raise NotImplementedError("Saturation blend mode is not implemented.")


def _blend_color(bg: Image.Image, fg: Image.Image) -> Image.Image:
    """ Color blend mode. """
    raise NotImplementedError("Color blend mode is not implemented.")


def _blend_luminosity(bg: Image.Image, fg: Image.Image) -> Image.Image:
    """ Luminosity blend mode. """
    raise NotImplementedError("Luminosity blend mode is not implemented.")


def _blend_addition(bg: Image.Image, fg: Image.Image) -> Image.Image:
    """ Addition blend mode. """
    raise NotImplementedError("Add blend mode is not implemented.")


def _blend_subtract(bg: Image.Image, fg: Image.Image) -> Image.Image:
    """ Subtract blend mode. """
    raise NotImplementedError("Subtract blend mode is not implemented.")


def _blend_divide(bg: Image.Image, fg: Image.Image) -> Image.Image:
    """ Divide blend mode. """
    raise NotImplementedError("Divide blend mode is not implemented.")
