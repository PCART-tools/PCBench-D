    def unique(self, level=None):
        if level is not None:
            self._validate_index_level(level)

        result = self._data.unique()
        return self._shallow_copy(result)
