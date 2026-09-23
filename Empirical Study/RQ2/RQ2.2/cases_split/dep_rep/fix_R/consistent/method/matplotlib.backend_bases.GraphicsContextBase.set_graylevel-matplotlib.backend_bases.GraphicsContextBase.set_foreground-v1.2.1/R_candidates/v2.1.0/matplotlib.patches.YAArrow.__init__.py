    @docstring.dedent_interpd
    def __init__(self, figure, xytip, xybase,
                 width=4, frac=0.1, headwidth=12, **kwargs):
        """
        Constructor arguments:

        *xytip*
          (*x*, *y*) location of arrow tip

        *xybase*
          (*x*, *y*) location the arrow base mid point

        *figure*
          The :class:`~matplotlib.figure.Figure` instance
          (fig.dpi)

        *width*
          The width of the arrow in points

        *frac*
          The fraction of the arrow length occupied by the head

        *headwidth*
          The width of the base of the arrow head in points

        Valid kwargs are:
        %(Patch)s

        """
        self.xytip = xytip
        self.xybase = xybase
        self.width = width
        self.frac = frac
        self.headwidth = headwidth
        Patch.__init__(self, **kwargs)
        # Set self.figure after Patch.__init__, since it sets self.figure to
        # None
        self.figure = figure
