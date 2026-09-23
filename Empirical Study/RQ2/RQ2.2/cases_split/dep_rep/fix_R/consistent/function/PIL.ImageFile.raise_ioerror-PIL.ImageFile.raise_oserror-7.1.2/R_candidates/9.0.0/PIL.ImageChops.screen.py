def screen(image1, image2):
    """
    Superimposes two inverted images on top of each other.

    .. code-block:: python

        out = MAX - ((MAX - image1) * (MAX - image2) / MAX)

    :rtype: :py:class:`~PIL.Image.Image`
    """

    image1.load()
    image2.load()
    return image1._new(image1.im.chop_screen(image2.im))
