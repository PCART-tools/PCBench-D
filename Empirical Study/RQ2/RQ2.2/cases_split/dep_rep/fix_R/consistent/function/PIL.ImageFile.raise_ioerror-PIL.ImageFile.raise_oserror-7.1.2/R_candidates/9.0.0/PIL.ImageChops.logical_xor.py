def logical_xor(image1, image2):
    """Logical XOR between two images.

    Both of the images must have mode "1".

    .. code-block:: python

        out = ((bool(image1) != bool(image2)) % MAX)

    :rtype: :py:class:`~PIL.Image.Image`
    """

    image1.load()
    image2.load()
    return image1._new(image1.im.chop_xor(image2.im))
