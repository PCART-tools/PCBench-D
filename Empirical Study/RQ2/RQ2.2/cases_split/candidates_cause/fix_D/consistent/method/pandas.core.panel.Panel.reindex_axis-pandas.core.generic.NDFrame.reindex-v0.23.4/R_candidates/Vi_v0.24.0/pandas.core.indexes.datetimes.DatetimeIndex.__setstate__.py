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

                freq = own_state[1]
                tz = timezones.tz_standardize(own_state[2])
                dtype = tz_to_dtype(tz)
                dtarr = DatetimeArray._simple_new(data, freq=freq, dtype=dtype)

                self.name = own_state[0]

            else:  # pragma: no cover
                data = np.empty(state)
                np.ndarray.__setstate__(data, state)
                dtarr = DatetimeArray(data)

            self._data = dtarr
            self._reset_identity()

        else:
            raise Exception("invalid pickle state")
