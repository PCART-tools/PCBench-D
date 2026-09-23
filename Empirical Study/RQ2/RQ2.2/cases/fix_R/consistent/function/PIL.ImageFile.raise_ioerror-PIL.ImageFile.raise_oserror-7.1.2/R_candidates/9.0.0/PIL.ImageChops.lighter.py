def lighter(image1, image2):
    """
    Compares the two images, pixel by pixel, and returns a new image containing
    the lighter values.

    .. code-block:: python

        out = max(image1, image2)

    :rtype: :py:class:`~PIL.Image.Image`
    """

    image1.load()
    image2.load()
    return image1._new(image1.im.chop_lighter(image2.im))
