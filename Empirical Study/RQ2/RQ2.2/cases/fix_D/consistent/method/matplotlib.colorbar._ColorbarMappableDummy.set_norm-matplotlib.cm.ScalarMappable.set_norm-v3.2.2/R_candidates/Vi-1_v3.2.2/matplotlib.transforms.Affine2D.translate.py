    def translate(self, tx, ty):
        """
        Adds a translation in place.

        Returns *self*, so this method can easily be chained with more
        calls to :meth:`rotate`, :meth:`rotate_deg`, :meth:`translate`
        and :meth:`scale`.
        """
        translate_mtx = np.array(
            [[1.0, 0.0, tx], [0.0, 1.0, ty], [0.0, 0.0, 1.0]], float)
        self._mtx = np.dot(translate_mtx, self._mtx)
        self.invalidate()
        return self
