    def _cumcount_array(self, arr, **kwargs):
        ascending = kwargs.pop('ascending', True)

        len_index = len(self.obj.index)
        cumcounts = np.zeros(len_index, dtype='int64')
        if ascending:
            for v in self.indices.values():
                cumcounts[v] = arr[:len(v)]
        else:
            for v in self.indices.values():
                cumcounts[v] = arr[len(v)-1::-1]
        return cumcounts
