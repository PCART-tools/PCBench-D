    def _get_pixel_distance_along_axis(self, where, perturb):
        """
        Returns the amount, in data coordinates, that a single pixel
        corresponds to in the locality given by *where*, which is also given
        in data coordinates, and is a y coordinate.

        *perturb* is the amount to perturb the pixel.  Usually +0.5 or -0.5.

        Implementing this routine for an axis is optional; if present, it will
        ensure that no ticks are lost due to round-off at the extreme ends of
        an axis.
        """

        #
        # first figure out the pixel location of the "where" point.  We use
        # 1e-10 for the x point, so that we remain compatible with log axes.

        # transformation from data coords to display coords
        trans = self.axes.transData
        # transformation from display coords to data coords
        transinv = trans.inverted()
        pix = trans.transform_point((1e-10, where))
        # perturb the pixel
        ptp = transinv.transform_point((pix[0], pix[1] + perturb))
        dy = abs(ptp[1] - where)
        return dy
