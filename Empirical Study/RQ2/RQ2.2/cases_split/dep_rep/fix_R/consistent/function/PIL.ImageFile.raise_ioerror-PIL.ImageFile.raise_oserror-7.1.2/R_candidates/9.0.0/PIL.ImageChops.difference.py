def difference(image1, image2):
    """
    Returns the absolute value of the pixel-by-pixel difference between the two
    images.

    .. code-block:: python

        out = abs(image1 - image2)

    :rtype: :py:class:`~PIL.Image.Image`
    """

    image1.load()
    image2.load()
    return image1._new(image1.im.chop_difference(image2.im))
