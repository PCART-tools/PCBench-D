    def _mode(self, dropna: bool = True) -> Categorical:
        codes = self._codes
        if dropna:
            good = self._codes != -1
            codes = self._codes[good]

        codes = htable.mode(codes, dropna)
        codes.sort()
        codes = coerce_indexer_dtype(codes, self.dtype.categories)
        return self._from_backing_data(codes)
