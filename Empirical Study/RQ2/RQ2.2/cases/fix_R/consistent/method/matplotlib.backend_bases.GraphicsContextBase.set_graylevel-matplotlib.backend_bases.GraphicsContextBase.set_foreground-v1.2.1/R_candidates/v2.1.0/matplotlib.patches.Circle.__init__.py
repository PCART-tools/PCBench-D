    @docstring.dedent_interpd
    def __init__(self, xy, radius=5, **kwargs):
        """
        Create true circle at center *xy* = (*x*, *y*) with given
        *radius*.  Unlike :class:`~matplotlib.patches.CirclePolygon`
        which is a polygonal approximation, this uses Bézier splines
        and is much closer to a scale-free circle.

        Valid kwargs are:
        %(Patch)s

        """
        Ellipse.__init__(self, xy, radius * 2, radius * 2, **kwargs)
        self.radius = radius
