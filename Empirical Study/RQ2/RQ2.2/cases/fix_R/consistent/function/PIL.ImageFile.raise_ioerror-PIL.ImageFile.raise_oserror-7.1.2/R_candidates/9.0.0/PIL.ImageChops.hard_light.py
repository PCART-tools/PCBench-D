def hard_light(image1, image2):
    """
    Superimposes two images on top of each other using the Hard Light algorithm

    :rtype: :py:class:`~PIL.Image.Image`
    """

    image1.load()
    image2.load()
    return image1._new(image1.im.chop_hard_light(image2.im))
