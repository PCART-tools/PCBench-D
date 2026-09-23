    def _internal_get_values(self):
        # override base Index version to get the numpy array representation of
        # the underlying Categorical
        return self._data._internal_get_values()
