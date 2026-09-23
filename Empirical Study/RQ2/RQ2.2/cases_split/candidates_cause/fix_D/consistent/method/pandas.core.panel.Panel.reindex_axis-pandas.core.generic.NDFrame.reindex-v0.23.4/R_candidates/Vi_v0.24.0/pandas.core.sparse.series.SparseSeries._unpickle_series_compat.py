    def _unpickle_series_compat(self, state):

        nd_state, own_state = state

        # recreate the ndarray
        data = np.empty(nd_state[1], dtype=nd_state[2])
        np.ndarray.__setstate__(data, nd_state)

        index, fill_value, sp_index = own_state[:3]
        name = None
        if len(own_state) > 3:
            name = own_state[3]

        # create a sparse array
        if not isinstance(data, SparseArray):
            data = SparseArray(data, sparse_index=sp_index,
                               fill_value=fill_value, copy=False)

        # recreate
        data = SingleBlockManager(data, index, fastpath=True)
        generic.NDFrame.__init__(self, data)

        self._set_axis(0, index)
        self.name = name
