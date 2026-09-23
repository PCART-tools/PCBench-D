    def clear(self):
        """
        Reset the underlying matrix to the identity transform.
        """
        # A bit faster than np.identity(3).
        self._mtx = IdentityTransform._mtx.copy()
        self.invalidate()
        return self
