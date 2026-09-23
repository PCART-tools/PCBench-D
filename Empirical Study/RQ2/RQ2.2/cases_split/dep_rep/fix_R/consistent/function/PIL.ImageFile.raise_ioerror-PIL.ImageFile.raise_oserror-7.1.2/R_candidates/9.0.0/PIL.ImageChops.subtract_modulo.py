def subtract_modulo(image1, image2):
    """Subtract two images, without clipping the result.

    .. code-block:: python

        out = ((image1 - image2) % MAX)

    :rtype: :py:class:`~PIL.Image.Image`
    """

    image1.load()
    image2.load()
    return image1._new(image1.im.chop_subtract_modulo(image2.im))
