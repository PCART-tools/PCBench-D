    def __getitem__(self, key):
        result = self._data[key]
        if isinstance(result, type(self._data)):
            return type(self)(result, name=self.name)

        # Includes cases where we get a 2D ndarray back for MPL compat
        deprecate_ndim_indexing(result)
        return result
