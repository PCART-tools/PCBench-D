    @property
    def ndim(self):
        if getattr(self, '_ndim', None) is None:
            self._ndim = len(self.axes)
        return self._ndim
