def linear_gradient(mode):
    """
    Generate 256x256 linear gradient from black to white, top to bottom.

    :param mode: Input mode.
    """
    return Image()._new(core.linear_gradient(mode))
