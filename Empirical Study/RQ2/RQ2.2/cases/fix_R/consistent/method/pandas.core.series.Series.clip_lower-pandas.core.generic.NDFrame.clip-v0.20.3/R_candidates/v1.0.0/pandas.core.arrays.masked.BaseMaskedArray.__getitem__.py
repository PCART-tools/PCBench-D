    def __getitem__(self, item):
        if is_integer(item):
            if self._mask[item]:
                return self.dtype.na_value
            return self._data[item]

        item = check_array_indexer(self, item)

        return type(self)(self._data[item], self._mask[item])
