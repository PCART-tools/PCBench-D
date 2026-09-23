    def skew(self, xShear, yShear):
        """
        Add a skew in place.

        *xShear* and *yShear* are the shear angles along the *x*- and
        *y*-axes, respectively, in radians.

        Returns *self*, so this method can easily be chained with more
        calls to :meth:`rotate`, :meth:`rotate_deg`, :meth:`translate`
        and :meth:`scale`.
        """
        rx = math.tan(xShear)
        ry = math.tan(yShear)
        mtx = self._mtx
        # Operating and assigning one scalar at a time is much faster.
        (xx, xy, x0), (yx, yy, y0), _ = mtx.tolist()
        # mtx = [[1 rx 0], [ry 1 0], [0 0 1]] * mtx
        mtx[0, 0] += rx * yx
        mtx[0, 1] += rx * yy
        mtx[0, 2] += rx * y0
        mtx[1, 0] += ry * xx
        mtx[1, 1] += ry * xy
        mtx[1, 2] += ry * x0
        self.invalidate()
        return self
