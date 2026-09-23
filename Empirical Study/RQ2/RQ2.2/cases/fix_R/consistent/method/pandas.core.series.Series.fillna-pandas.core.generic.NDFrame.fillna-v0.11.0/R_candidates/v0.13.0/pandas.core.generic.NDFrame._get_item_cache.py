    def _get_item_cache(self, item):
        cache = self._item_cache
        res = cache.get(item)
        if res is None:
            values = self._data.get(item)
            res = self._box_item_values(item, values)
            cache[item] = res
            res._cacher = (item, weakref.ref(self))
        return res
