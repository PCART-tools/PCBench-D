    @property
    def dtype(self):
        return IntervalDtype(self.left.dtype)
