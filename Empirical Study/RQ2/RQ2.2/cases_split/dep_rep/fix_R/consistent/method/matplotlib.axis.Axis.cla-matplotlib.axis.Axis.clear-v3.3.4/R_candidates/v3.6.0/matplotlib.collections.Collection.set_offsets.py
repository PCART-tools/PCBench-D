    def set_offsets(self, offsets):
        """
        Set the offsets for the collection.

        Parameters
        ----------
        offsets : (N, 2) or (2,) array-like
        """
        offsets = np.asanyarray(offsets)
        if offsets.shape == (2,):  # Broadcast (2,) -> (1, 2) but nothing else.
            offsets = offsets[None, :]
        self._offsets = np.column_stack(
            (np.asarray(self.convert_xunits(offsets[:, 0]), 'float'),
             np.asarray(self.convert_yunits(offsets[:, 1]), 'float')))
        self.stale = True
