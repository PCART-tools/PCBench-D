    def _unpickle_series_compat(self, state):
        if isinstance(state, dict):
            self._data = state['_data']
            self.name = state['name']
            self.index = self._data.index

        elif isinstance(state, tuple):

            # < 0.12 series pickle

            nd_state, own_state = state

            # recreate the ndarray
            data = np.empty(nd_state[1], dtype=nd_state[2])
            np.ndarray.__setstate__(data, nd_state)

            # backwards compat
            index, name = own_state[0], None
            if len(own_state) > 1:
                name = own_state[1]

            # recreate
            self._data = SingleBlockManager(data, index, fastpath=True)
            self._index = index
            self.name = name

        else:
            raise Exception("cannot unpickle legacy formats -> [%s]" % state)
