    def __init__(self, ax, *args, **kwargs):
        """
        Draw triangular grid contour lines or filled regions,
        depending on whether keyword arg 'filled' is False
        (default) or True.

        The first argument of the initializer must be an axes
        object.  The remaining arguments and keyword arguments
        are described in the docstring of `tricontour`.
        """
        ContourSet.__init__(self, ax, *args, **kwargs)
