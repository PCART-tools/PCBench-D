    @cbook.deprecated("3.1")
    def set_active(self, ind):
        self._ind = ind
        self._active = [self._axes[i] for i in self._ind]
