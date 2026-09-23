def logical_and(image1, image2):
    """Logical AND between two images.

    Both of the images must have mode "1". If you would like to perform a
    logical AND on an image with a mode other than "1", try
    :py:meth:`~PIL.ImageChops.multiply` instead, using a black-and-white mask
    as the second image.

    .. code-block:: python

        out = ((image1 and image2) % MAX)

    :rtype: :py:class:`~PIL.Image.Image`
    """

    image1.load()
    image2.load()
    return image1._new(image1.im.chop_and(image2.im))
