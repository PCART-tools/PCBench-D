    def clear(self):
        """
        Reset the underlying matrix to the identity transform.
        """
        self._mtx = np.identity(3)
        self.invalidate()
        return self
