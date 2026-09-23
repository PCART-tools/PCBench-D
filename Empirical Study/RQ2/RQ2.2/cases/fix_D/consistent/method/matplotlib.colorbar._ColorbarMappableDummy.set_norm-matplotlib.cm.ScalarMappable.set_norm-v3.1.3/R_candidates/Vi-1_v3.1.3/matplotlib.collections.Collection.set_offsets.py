    def set_offsets(self, offsets):
        """
        Set the offsets for the collection.

        Parameters
        ----------
        offsets : float or sequence of floats
        """
        offsets = np.asanyarray(offsets, float)
        if offsets.shape == (2,):  # Broadcast (2,) -> (1, 2) but nothing else.
            offsets = offsets[None, :]
        # This decision is based on how they are initialized above in __init__.
        if self._uniform_offsets is None:
            self._offsets = offsets
        else:
            self._uniform_offsets = offsets
        self.stale = True
