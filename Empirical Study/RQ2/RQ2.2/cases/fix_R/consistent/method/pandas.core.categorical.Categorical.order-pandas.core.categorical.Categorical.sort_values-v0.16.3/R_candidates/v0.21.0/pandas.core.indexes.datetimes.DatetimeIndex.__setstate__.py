    def __setstate__(self, state):
        """Necessary for making this object picklable"""
        if isinstance(state, dict):
            super(DatetimeIndex, self).__setstate__(state)

        elif isinstance(state, tuple):

            # < 0.15 compat
            if len(state) == 2:
                nd_state, own_state = state
                data = np.empty(nd_state[1], dtype=nd_state[2])
                np.ndarray.__setstate__(data, nd_state)

                self.name = own_state[0]
                self.offset = own_state[1]
                self.tz = own_state[2]

                # provide numpy < 1.7 compat
                if nd_state[2] == 'M8[us]':
                    new_state = np.ndarray.__reduce__(data.astype('M8[ns]'))
                    np.ndarray.__setstate__(data, new_state[2])

            else:  # pragma: no cover
                data = np.empty(state)
                np.ndarray.__setstate__(data, state)

            self._data = data
            self._reset_identity()

        else:
            raise Exception("invalid pickle state")
