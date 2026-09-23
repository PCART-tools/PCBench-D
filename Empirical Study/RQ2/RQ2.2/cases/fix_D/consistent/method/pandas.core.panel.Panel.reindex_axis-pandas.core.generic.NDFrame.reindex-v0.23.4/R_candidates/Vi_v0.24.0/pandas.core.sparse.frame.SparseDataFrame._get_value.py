    def _get_value(self, index, col, takeable=False):
        if takeable is True:
            series = self._iget_item_cache(col)
        else:
            series = self._get_item_cache(col)

        return series._get_value(index, takeable=takeable)
