    @_docstring.dedent_interpd
    @_api.make_keyword_only("3.6", name="closed")
    def __init__(self, xy, closed=True, **kwargs):
        """
        *xy* is a numpy array with shape Nx2.

        If *closed* is *True*, the polygon will be closed so the
        starting and ending points are the same.

        Valid keyword arguments are:

        %(Patch:kwdoc)s
        """
        super().__init__(**kwargs)
        self._closed = closed
        self.set_xy(xy)
