    def _get_unique_index(self, dropna=False):
        if self.is_unique and not dropna:
            return self

        result = self._data.unique()
        if dropna and self.hasnans:
            result = result[~result.isna()]
        return self._shallow_copy(result)
