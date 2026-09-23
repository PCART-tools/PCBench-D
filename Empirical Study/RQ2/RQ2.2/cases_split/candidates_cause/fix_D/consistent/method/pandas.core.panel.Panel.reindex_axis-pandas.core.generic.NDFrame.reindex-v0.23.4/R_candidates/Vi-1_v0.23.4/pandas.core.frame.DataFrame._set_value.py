    def _set_value(self, index, col, value, takeable=False):
        try:
            if takeable is True:
                series = self._iget_item_cache(col)
                return series._set_value(index, value, takeable=True)

            series = self._get_item_cache(col)
            engine = self.index._engine
            engine.set_value(series._values, index, value)
            return self
        except (KeyError, TypeError):

            # set using a non-recursive method & reset the cache
            self.loc[index, col] = value
            self._item_cache.pop(col, None)

            return self
