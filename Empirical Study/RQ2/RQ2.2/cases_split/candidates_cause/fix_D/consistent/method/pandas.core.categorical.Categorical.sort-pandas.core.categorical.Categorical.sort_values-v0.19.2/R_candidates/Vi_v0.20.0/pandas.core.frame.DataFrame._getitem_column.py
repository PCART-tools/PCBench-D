    def _getitem_column(self, key):
        """ return the actual column """

        # get column
        if self.columns.is_unique:
            return self._get_item_cache(key)

        # duplicate columns & possible reduce dimensionality
        result = self._constructor(self._data.get(key))
        if result.columns.is_unique:
            result = result[key]

        return result
