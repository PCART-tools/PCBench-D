    def _cumcount_array(self, arr=None, **kwargs):
        """
        arr is where cumcount gets its values from

        note: this is currently implementing sort=False (though the default is sort=True)
              for groupby in general
        """
        ascending = kwargs.pop('ascending', True)

        if arr is None:
            arr = np.arange(self.grouper._max_groupsize, dtype='int64')

        len_index = len(self._selected_obj.index)
        cumcounts = np.zeros(len_index, dtype=arr.dtype)
        if not len_index:
            return cumcounts

        indices, values = [], []
        for v in self.indices.values():
            indices.append(v)

            if ascending:
                values.append(arr[:len(v)])
            else:
                values.append(arr[len(v)-1::-1])

        indices = np.concatenate(indices)
        values = np.concatenate(values)
        cumcounts[indices] = values

        return cumcounts
