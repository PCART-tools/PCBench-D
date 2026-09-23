    @extents.setter
    def extents(self, extents):
        self._set_extents(extents)
        self._selection_completed = True
