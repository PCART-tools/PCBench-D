    def padded(self, w_pad, h_pad=None):
        """
        Construct a `Bbox` by padding this one on all four sides.

        Parameters
        ----------
        w_pad : float
            Width pad
        h_pad : float, optional
            Height pad.  Defaults to *w_pad*.

        """
        points = self.get_points()
        if h_pad is None:
            h_pad = w_pad
        return Bbox(points + [[-w_pad, -h_pad], [w_pad, h_pad]])
