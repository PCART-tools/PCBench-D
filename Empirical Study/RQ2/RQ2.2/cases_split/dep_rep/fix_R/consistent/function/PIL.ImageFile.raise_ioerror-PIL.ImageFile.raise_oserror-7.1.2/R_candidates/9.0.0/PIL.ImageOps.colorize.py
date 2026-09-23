def colorize(image, black, white, mid=None, blackpoint=0, whitepoint=255, midpoint=127):
    """
    Colorize grayscale image.
    This function calculates a color wedge which maps all black pixels in
    the source image to the first color and all white pixels to the
    second color. If ``mid`` is specified, it uses three-color mapping.
    The ``black`` and ``white`` arguments should be RGB tuples or color names;
    optionally you can use three-color mapping by also specifying ``mid``.
    Mapping positions for any of the colors can be specified
    (e.g. ``blackpoint``), where these parameters are the integer
    value corresponding to where the corresponding color should be mapped.
    These parameters must have logical order, such that
    ``blackpoint <= midpoint <= whitepoint`` (if ``mid`` is specified).

    :param image: The image to colorize.
    :param black: The color to use for black input pixels.
    :param white: The color to use for white input pixels.
    :param mid: The color to use for midtone input pixels.
    :param blackpoint: an int value [0, 255] for the black mapping.
    :param whitepoint: an int value [0, 255] for the white mapping.
    :param midpoint: an int value [0, 255] for the midtone mapping.
    :return: An image.
    """

    # Initial asserts
    assert image.mode == "L"
    if mid is None:
        assert 0 <= blackpoint <= whitepoint <= 255
    else:
        assert 0 <= blackpoint <= midpoint <= whitepoint <= 255

    # Define colors from arguments
    black = _color(black, "RGB")
    white = _color(white, "RGB")
    if mid is not None:
        mid = _color(mid, "RGB")

    # Empty lists for the mapping
    red = []
    green = []
    blue = []

    # Create the low-end values
    for i in range(0, blackpoint):
        red.append(black[0])
        green.append(black[1])
        blue.append(black[2])

    # Create the mapping (2-color)
    if mid is None:

        range_map = range(0, whitepoint - blackpoint)

        for i in range_map:
            red.append(black[0] + i * (white[0] - black[0]) // len(range_map))
            green.append(black[1] + i * (white[1] - black[1]) // len(range_map))
            blue.append(black[2] + i * (white[2] - black[2]) // len(range_map))

    # Create the mapping (3-color)
    else:

        range_map1 = range(0, midpoint - blackpoint)
        range_map2 = range(0, whitepoint - midpoint)

        for i in range_map1:
            red.append(black[0] + i * (mid[0] - black[0]) // len(range_map1))
            green.append(black[1] + i * (mid[1] - black[1]) // len(range_map1))
            blue.append(black[2] + i * (mid[2] - black[2]) // len(range_map1))
        for i in range_map2:
            red.append(mid[0] + i * (white[0] - mid[0]) // len(range_map2))
            green.append(mid[1] + i * (white[1] - mid[1]) // len(range_map2))
            blue.append(mid[2] + i * (white[2] - mid[2]) // len(range_map2))

    # Create the high-end values
    for i in range(0, 256 - whitepoint):
        red.append(white[0])
        green.append(white[1])
        blue.append(white[2])

    # Return converted image
    image = image.convert("RGB")
    return _lut(image, red + green + blue)
