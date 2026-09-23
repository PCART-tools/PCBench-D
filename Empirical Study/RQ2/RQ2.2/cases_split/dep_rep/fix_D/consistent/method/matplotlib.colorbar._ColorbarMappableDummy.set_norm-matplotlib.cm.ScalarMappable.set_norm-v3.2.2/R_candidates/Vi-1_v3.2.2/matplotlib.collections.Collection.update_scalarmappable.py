    def update_scalarmappable(self):
        """Update colors from the scalar mappable array, if it is not None."""
        if self._A is None:
            return
        if self._A.ndim > 1:
            raise ValueError('Collections can only map rank 1 arrays')
        if not self.check_update("array"):
            return
        if self._is_filled:
            self._facecolors = self.to_rgba(self._A, self._alpha)
        elif self._is_stroked:
            self._edgecolors = self.to_rgba(self._A, self._alpha)
        self.stale = True
