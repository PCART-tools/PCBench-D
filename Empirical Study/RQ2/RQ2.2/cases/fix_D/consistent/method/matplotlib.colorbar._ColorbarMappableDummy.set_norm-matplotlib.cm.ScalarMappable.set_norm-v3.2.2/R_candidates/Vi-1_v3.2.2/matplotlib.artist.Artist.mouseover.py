    @mouseover.setter
    def mouseover(self, val):
        val = bool(val)
        self._mouseover = val
        ax = self.axes
        if ax:
            if val:
                ax._mouseover_set.add(self)
            else:
                ax._mouseover_set.discard(self)
