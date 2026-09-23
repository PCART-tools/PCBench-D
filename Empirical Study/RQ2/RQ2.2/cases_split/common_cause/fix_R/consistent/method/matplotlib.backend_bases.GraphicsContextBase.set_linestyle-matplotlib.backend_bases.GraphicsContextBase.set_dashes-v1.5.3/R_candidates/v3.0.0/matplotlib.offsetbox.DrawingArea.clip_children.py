    @clip_children.setter
    def clip_children(self, val):
        self._clip_children = bool(val)
        self.stale = True
