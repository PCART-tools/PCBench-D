    @property
    def group_index(self):
        if self._group_index is None:
            self._make_labels()
        return self._group_index
