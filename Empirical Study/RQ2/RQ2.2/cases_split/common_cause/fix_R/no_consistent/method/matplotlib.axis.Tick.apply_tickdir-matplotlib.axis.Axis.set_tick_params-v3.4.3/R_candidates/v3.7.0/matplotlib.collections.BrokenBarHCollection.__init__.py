    def __init__(self, xranges, yrange, **kwargs):
        """
        Parameters
        ----------
        xranges : list of (float, float)
            The sequence of (left-edge-position, width) pairs for each bar.
        yrange : (float, float)
            The (lower-edge, height) common to all bars.
        **kwargs
            Forwarded to `.Collection`.
        """
        ymin, ywidth = yrange
        ymax = ymin + ywidth
        verts = [[(xmin, ymin),
                  (xmin, ymax),
                  (xmin + xwidth, ymax),
                  (xmin + xwidth, ymin),
                  (xmin, ymin)] for xmin, xwidth in xranges]
        super().__init__(verts, **kwargs)
