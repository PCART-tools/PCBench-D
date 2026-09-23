def invert(image):
    """
    Invert (negate) the image.

    :param image: The image to invert.
    :return: An image.
    """
    lut = []
    for i in range(256):
        lut.append(255 - i)
    return _lut(image, lut)
