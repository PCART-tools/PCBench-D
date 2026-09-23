    def __getitem__(self, item: PositionalIndexer) -> Self | Any:
        item = check_array_indexer(self, item)

        newmask = self._mask[item]
        if is_bool(newmask):
            # This is a scalar indexing
            if newmask:
                return self.dtype.na_value
            return self._data[item]

        return self._simple_new(self._data[item], newmask)
