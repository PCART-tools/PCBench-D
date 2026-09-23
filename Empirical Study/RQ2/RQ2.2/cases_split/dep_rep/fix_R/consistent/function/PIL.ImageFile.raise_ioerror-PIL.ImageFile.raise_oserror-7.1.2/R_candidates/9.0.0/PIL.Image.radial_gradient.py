def radial_gradient(mode):
    """
    Generate 256x256 radial gradient from black to white, centre to edge.

    :param mode: Input mode.
    """
    return Image()._new(core.radial_gradient(mode))
