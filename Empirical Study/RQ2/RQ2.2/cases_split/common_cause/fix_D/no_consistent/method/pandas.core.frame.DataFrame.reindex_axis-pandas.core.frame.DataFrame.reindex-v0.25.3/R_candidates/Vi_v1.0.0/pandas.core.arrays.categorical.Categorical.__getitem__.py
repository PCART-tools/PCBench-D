    def __getitem__(self, key):
        """
        Return an item.
        """
        if isinstance(key, (int, np.integer)):
            i = self._codes[key]
            if i == -1:
                return np.nan
            else:
                return self.categories[i]

        key = check_array_indexer(self, key)

        result = self._codes[key]
        if result.ndim > 1:
            deprecate_ndim_indexing(result)
            return result
        return self._constructor(result, dtype=self.dtype, fastpath=True)
