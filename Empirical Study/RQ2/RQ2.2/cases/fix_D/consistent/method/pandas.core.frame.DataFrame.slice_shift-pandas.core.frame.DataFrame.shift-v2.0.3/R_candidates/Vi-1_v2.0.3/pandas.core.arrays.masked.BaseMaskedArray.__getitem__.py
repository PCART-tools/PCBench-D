    def __getitem__(
        self: BaseMaskedArrayT, item: PositionalIndexer
    ) -> BaseMaskedArrayT | Any:
        item = check_array_indexer(self, item)

        newmask = self._mask[item]
        if is_bool(newmask):
            # This is a scalar indexing
            if newmask:
                return self.dtype.na_value
            return self._data[item]

        return type(self)(self._data[item], newmask)
