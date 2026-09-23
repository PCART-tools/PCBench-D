    def _get_item_cache(self, item: Hashable) -> Series:
        """Return the cached item, item represents a label indexer."""
        if using_copy_on_write():
            loc = self.columns.get_loc(item)
            return self._ixs(loc, axis=1)

        cache = self._item_cache
        res = cache.get(item)
        if res is None:
            # All places that call _get_item_cache have unique columns,
            #  pending resolution of GH#33047

            loc = self.columns.get_loc(item)
            res = self._ixs(loc, axis=1)

            cache[item] = res

            # for a chain
            res._is_copy = self._is_copy
        return res
