    @docstring.dedent_interpd
    def __init__(self, xy, closed=True, **kwargs):
        """
        *xy* is a numpy array with shape Nx2.

        If *closed* is *True*, the polygon will be closed so the
        starting and ending points are the same.

        Valid kwargs are:
        %(Patch)s
        """
        Patch.__init__(self, **kwargs)
        self._closed = closed
        self.set_xy(xy)
