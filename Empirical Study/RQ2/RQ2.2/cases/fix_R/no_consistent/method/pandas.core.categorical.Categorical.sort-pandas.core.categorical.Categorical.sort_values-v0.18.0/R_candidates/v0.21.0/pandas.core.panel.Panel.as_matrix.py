    def as_matrix(self):
        self._consolidate_inplace()
        return self._data.as_matrix()
