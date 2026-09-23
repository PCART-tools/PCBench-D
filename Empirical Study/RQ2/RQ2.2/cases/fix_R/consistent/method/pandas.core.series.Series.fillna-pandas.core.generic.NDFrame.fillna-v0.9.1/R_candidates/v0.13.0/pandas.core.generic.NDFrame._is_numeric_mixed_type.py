    @property
    def _is_numeric_mixed_type(self):
        f = lambda: self._data.is_numeric_mixed_type
        return self._protect_consolidate(f)
