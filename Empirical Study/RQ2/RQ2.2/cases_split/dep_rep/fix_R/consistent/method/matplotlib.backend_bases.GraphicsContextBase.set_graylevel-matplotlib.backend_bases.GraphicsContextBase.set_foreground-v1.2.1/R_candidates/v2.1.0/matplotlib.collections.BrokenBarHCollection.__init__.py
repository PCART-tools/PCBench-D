    @docstring.dedent_interpd
    def __init__(self, xranges, yrange, **kwargs):
        """
        *xranges*
            sequence of (*xmin*, *xwidth*)

        *yrange*
            *ymin*, *ywidth*

        %(Collection)s
        """
        ymin, ywidth = yrange
        ymax = ymin + ywidth
        verts = [[(xmin, ymin),
                  (xmin, ymax),
                  (xmin + xwidth, ymax),
                  (xmin + xwidth, ymin),
                  (xmin, ymin)] for xmin, xwidth in xranges]
        PolyCollection.__init__(self, verts, **kwargs)
