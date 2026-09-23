    def _iget_item_cache(self, item):
        """Return the cached item, item represents a positional indexer."""
        ax = self._info_axis
        if ax.is_unique:
            lower = self._get_item_cache(ax[item])
        else:
            lower = self._take_with_is_copy(item, axis=self._info_axis_number)
        return lower
