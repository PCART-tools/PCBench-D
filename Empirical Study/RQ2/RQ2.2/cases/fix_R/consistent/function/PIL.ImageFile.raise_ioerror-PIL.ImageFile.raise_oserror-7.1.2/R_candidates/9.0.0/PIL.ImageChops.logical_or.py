def logical_or(image1, image2):
    """Logical OR between two images.

    Both of the images must have mode "1".

    .. code-block:: python

        out = ((image1 or image2) % MAX)

    :rtype: :py:class:`~PIL.Image.Image`
    """

    image1.load()
    image2.load()
    return image1._new(image1.im.chop_or(image2.im))
