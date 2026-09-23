    @property
    def depth(self):
        return max(self._x.depth, self._y.depth)
