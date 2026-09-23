    def scale(self, sx, sy=None):
        """
        Adds a scale in place.

        If *sy* is None, the same scale is applied in both the *x*- and
        *y*-directions.

        Returns *self*, so this method can easily be chained with more
        calls to :meth:`rotate`, :meth:`rotate_deg`, :meth:`translate`
        and :meth:`scale`.
        """
        if sy is None:
            sy = sx
        scale_mtx = np.array(
            [[sx, 0.0, 0.0], [0.0, sy, 0.0], [0.0, 0.0, 1.0]], float)
        self._mtx = np.dot(scale_mtx, self._mtx)
        self.invalidate()
        return self
