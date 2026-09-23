def _check_size(size):
    """
    Common check to enforce type and sanity check on size tuples

    :param size: Should be a 2 tuple of (width, height)
    :returns: True, or raises a ValueError
    """

    if not isinstance(size, (list, tuple)):
        raise ValueError("Size must be a tuple")
    if len(size) != 2:
        raise ValueError("Size must be a tuple of length 2")
    if size[0] < 0 or size[1] < 0:
        raise ValueError("Width and height must be >= 0")

    return True
