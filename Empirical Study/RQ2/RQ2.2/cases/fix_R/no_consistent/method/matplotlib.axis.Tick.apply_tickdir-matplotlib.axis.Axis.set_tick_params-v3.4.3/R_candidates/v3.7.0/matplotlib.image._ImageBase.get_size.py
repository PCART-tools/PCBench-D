    def get_size(self):
        """Return the size of the image as tuple (numrows, numcols)."""
        if self._A is None:
            raise RuntimeError('You must first set the image array')

        return self._A.shape[:2]
