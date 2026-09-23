    @_docstring.dedent_interpd
    def __init__(self, xy, radius=5, *,
                 resolution=20,  # the number of vertices
                 ** kwargs):
        """
        Create a circle at *xy* = (*x*, *y*) with given *radius*.

        This circle is approximated by a regular polygon with *resolution*
        sides.  For a smoother circle drawn with splines, see `Circle`.

        Valid keyword arguments are:

        %(Patch:kwdoc)s
        """
        super().__init__(
            xy, resolution, radius=radius, orientation=0, **kwargs)
