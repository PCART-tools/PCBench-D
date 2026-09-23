def subtract(image1, image2, scale=1.0, offset=0):
    """
    Subtracts two images, dividing the result by scale and adding the offset.
    If omitted, scale defaults to 1.0, and offset to 0.0.

    .. code-block:: python

        out = ((image1 - image2) / scale + offset)

    :rtype: :py:class:`~PIL.Image.Image`
    """

    image1.load()
    image2.load()
    return image1._new(image1.im.chop_subtract(image2.im, scale, offset))
