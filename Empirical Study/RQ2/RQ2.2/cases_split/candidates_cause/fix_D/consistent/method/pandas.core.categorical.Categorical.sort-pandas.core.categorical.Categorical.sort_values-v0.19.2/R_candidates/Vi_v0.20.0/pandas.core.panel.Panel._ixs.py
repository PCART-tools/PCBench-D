    def _ixs(self, i, axis=0):
        """
        i : int, slice, or sequence of integers
        axis : int
        """

        ax = self._get_axis(axis)
        key = ax[i]

        # xs cannot handle a non-scalar key, so just reindex here
        # if we have a multi-index and a single tuple, then its a reduction
        # (GH 7516)
        if not (isinstance(ax, MultiIndex) and isinstance(key, tuple)):
            if is_list_like(key):
                indexer = {self._get_axis_name(axis): key}
                return self.reindex(**indexer)

        # a reduction
        if axis == 0:
            values = self._data.iget(i)
            return self._box_item_values(key, values)

        # xs by position
        self._consolidate_inplace()
        new_data = self._data.xs(i, axis=axis, copy=True, takeable=True)
        return self._construct_return_type(new_data)
