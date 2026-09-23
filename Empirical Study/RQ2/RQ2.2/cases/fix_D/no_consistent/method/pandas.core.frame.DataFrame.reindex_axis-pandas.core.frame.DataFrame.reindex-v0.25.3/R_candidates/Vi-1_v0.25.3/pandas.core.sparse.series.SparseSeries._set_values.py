    def _set_values(self, key, value):

        # this might be inefficient as we have to recreate the sparse array
        # rather than setting individual elements, but have to convert
        # the passed slice/boolean that's in dense space into a sparse indexer
        # not sure how to do that!
        if isinstance(key, Series):
            key = key.values

        values = self.values.to_dense()
        values[key] = libindex.convert_scalar(values, value)
        values = SparseArray(values, fill_value=self.fill_value, kind=self.kind)
        self._data = SingleBlockManager(values, self.index)
