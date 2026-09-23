    def _get_item_cache(self, item):
        """Return the cached item, item represents a label indexer."""
        cache = self._item_cache
        res = cache.get(item)
        if res is None:
            values = self._data.get(item)
            res = self._box_item_values(item, values)
            cache[item] = res
            res._set_as_cached(item, self)

            # for a chain
            res._is_copy = self._is_copy
        return res
