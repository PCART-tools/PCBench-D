def getcolor(color, mode):
    """
    Same as :py:func:`~PIL.ImageColor.getrgb`, but converts the RGB value to a
    greyscale value if the mode is not color or a palette image. If the string
    cannot be parsed, this function raises a :py:exc:`ValueError` exception.

    .. versionadded:: 1.1.4

    :param color: A color string
    :return: ``(graylevel [, alpha]) or (red, green, blue[, alpha])``
    """
    # same as getrgb, but converts the result to the given mode
    color, alpha = getrgb(color), 255
    if len(color) == 4:
        color, alpha = color[0:3], color[3]

    if Image.getmodebase(mode) == "L":
        r, g, b = color
        # ITU-R Recommendation 601-2 for nonlinear RGB
        # scaled to 24 bits to match the convert's implementation.
        color = (r * 19595 + g * 38470 + b * 7471 + 0x8000) >> 16
        if mode[-1] == "A":
            return (color, alpha)
    else:
        if mode[-1] == "A":
            return color + (alpha,)
    return color
