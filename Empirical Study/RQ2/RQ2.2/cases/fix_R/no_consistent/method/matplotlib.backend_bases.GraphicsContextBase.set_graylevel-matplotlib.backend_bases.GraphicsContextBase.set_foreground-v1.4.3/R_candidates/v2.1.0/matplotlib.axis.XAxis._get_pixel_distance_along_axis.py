    def _get_pixel_distance_along_axis(self, where, perturb):
        """
        Returns the amount, in data coordinates, that a single pixel
        corresponds to in the locality given by "where", which is also given
        in data coordinates, and is an x coordinate. "perturb" is the amount
        to perturb the pixel.  Usually +0.5 or -0.5.

        Implementing this routine for an axis is optional; if present, it will
        ensure that no ticks are lost due to round-off at the extreme ends of
        an axis.
        """

        # Note that this routine does not work for a polar axis, because of
        # the 1e-10 below.  To do things correctly, we need to use rmax
        # instead of 1e-10 for a polar axis.  But since we do not have that
        # kind of information at this point, we just don't try to pad anything
        # for the theta axis of a polar plot.
        if self.axes.name == 'polar':
            return 0.0

        #
        # first figure out the pixel location of the "where" point.  We use
        # 1e-10 for the y point, so that we remain compatible with log axes.

        # transformation from data coords to display coords
        trans = self.axes.transData
        # transformation from display coords to data coords
        transinv = trans.inverted()
        pix = trans.transform_point((where, 1e-10))
        # perturb the pixel
        ptp = transinv.transform_point((pix[0] + perturb, pix[1]))
        dx = abs(ptp[0] - where)

        return dx
