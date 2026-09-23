def blend(image1, image2, alpha):
    """Blend images using constant transparency weight. Alias for
    :py:func:`PIL.Image.blend`.

    :rtype: :py:class:`~PIL.Image.Image`
    """

    return Image.blend(image1, image2, alpha)
