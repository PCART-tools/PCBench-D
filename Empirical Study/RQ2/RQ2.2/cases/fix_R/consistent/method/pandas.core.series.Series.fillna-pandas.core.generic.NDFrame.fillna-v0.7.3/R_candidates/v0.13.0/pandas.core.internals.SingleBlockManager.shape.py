    @property
    def shape(self):
        if getattr(self, '_shape', None) is None:
            self._shape = tuple([len(self.axes[0])])
        return self._shape
