    @mouseover.setter
    def mouseover(self, val):
        val = bool(val)
        self._mouseover = val
        ax = self.axes
        if ax:
            if val:
                ax.mouseover_set.add(self)
            else:
                ax.mouseover_set.discard(self)
