    def _cumcount_array(self, arr=None, **kwargs):
        """
        arr is where cumcount gets it's values from
        """
        ascending = kwargs.pop('ascending', True)

        if arr is None:
            arr = np.arange(self.grouper._max_groupsize, dtype='int64')

        len_index = len(self._selected_obj.index)
        cumcounts = np.empty(len_index, dtype=arr.dtype)

        if ascending:
            for v in self.indices.values():
                cumcounts[v] = arr[:len(v)]
        else:
            for v in self.indices.values():
                cumcounts[v] = arr[len(v)-1::-1]
        return cumcounts
