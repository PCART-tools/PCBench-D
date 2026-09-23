    def unique(self, level=None):
        if level is not None:
            self._validate_index_level(level)

        result = self._data.unique()

        # Note: if `self` is already unique, then self.unique() should share
        #  a `freq` with self.  If not already unique, then self.freq must be
        #  None, so again sharing freq is correct.
        return self._shallow_copy(result._data)
