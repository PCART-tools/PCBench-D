def overlay(image1, image2):
    """
    Superimposes two images on top of each other using the Overlay algorithm

    :rtype: :py:class:`~PIL.Image.Image`
    """

    image1.load()
    image2.load()
    return image1._new(image1.im.chop_overlay(image2.im))
