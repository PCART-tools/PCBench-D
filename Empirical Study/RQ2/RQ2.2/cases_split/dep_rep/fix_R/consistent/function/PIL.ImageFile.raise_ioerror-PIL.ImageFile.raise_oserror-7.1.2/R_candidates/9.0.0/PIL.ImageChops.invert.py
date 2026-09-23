def invert(image):
    """
    Invert an image (channel).

    .. code-block:: python

        out = MAX - image

    :rtype: :py:class:`~PIL.Image.Image`
    """

    image.load()
    return image._new(image.im.chop_invert())
