    def skew(self, xShear, yShear):
        """
        Add a skew in place.

        *xShear* and *yShear* are the shear angles along the *x*- and
        *y*-axes, respectively, in radians.

        Returns *self*, so this method can easily be chained with more
        calls to :meth:`rotate`, :meth:`rotate_deg`, :meth:`translate`
        and :meth:`scale`.
        """
        rotX = math.tan(xShear)
        rotY = math.tan(yShear)
        skew_mtx = np.array(
            [[1.0, rotX, 0.0], [rotY, 1.0, 0.0], [0.0, 0.0, 1.0]], float)
        self._mtx = np.dot(skew_mtx, self._mtx)
        self.invalidate()
        return self
