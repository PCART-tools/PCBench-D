    def _ixs(self, i, axis=0):
        """
        i : int, slice, or sequence of integers
        axis : int
        """

        key = self._get_axis(axis)[i]

        # xs cannot handle a non-scalar key, so just reindex here
        if _is_list_like(key):
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
