def composite(image1, image2, mask):
    """Create composite using transparency mask. Alias for
    :py:func:`PIL.Image.composite`.

    :rtype: :py:class:`~PIL.Image.Image`
    """

    return Image.composite(image1, image2, mask)
