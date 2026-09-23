    def translate(self, tx, ty):
        """
        Add a translation in place.

        Returns *self*, so this method can easily be chained with more
        calls to :meth:`rotate`, :meth:`rotate_deg`, :meth:`translate`
        and :meth:`scale`.
        """
        self._mtx[0, 2] += tx
        self._mtx[1, 2] += ty
        self.invalidate()
        return self
