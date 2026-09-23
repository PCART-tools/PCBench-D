def posterize(image, bits):
    """
    Reduce the number of bits for each color channel.

    :param image: The image to posterize.
    :param bits: The number of bits to keep for each channel (1-8).
    :return: An image.
    """
    lut = []
    mask = ~(2 ** (8 - bits) - 1)
    for i in range(256):
        lut.append(i & mask)
    return _lut(image, lut)
