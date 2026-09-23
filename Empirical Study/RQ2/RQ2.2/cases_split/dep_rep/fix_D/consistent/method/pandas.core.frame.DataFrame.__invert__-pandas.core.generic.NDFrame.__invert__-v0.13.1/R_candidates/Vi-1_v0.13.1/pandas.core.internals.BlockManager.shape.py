    @property
    def shape(self):
        if getattr(self, '_shape', None) is None:
            self._shape = tuple(len(ax) for ax in self.axes)
        return self._shape
