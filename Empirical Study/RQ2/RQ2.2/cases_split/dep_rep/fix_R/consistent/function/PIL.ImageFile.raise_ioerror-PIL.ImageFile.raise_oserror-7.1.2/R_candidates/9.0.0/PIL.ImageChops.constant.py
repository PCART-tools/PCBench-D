def constant(image, value):
    """Fill a channel with a given grey level.

    :rtype: :py:class:`~PIL.Image.Image`
    """

    return Image.new("L", image.size, value)
