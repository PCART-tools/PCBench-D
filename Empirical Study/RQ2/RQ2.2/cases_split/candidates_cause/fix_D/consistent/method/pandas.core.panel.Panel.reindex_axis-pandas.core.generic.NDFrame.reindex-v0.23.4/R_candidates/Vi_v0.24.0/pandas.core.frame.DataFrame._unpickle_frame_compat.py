    def _unpickle_frame_compat(self, state):  # pragma: no cover
        if len(state) == 2:  # pragma: no cover
            series, idx = state
            columns = sorted(series)
        else:
            series, cols, idx = state
            columns = com._unpickle_array(cols)

        index = com._unpickle_array(idx)
        self._data = self._init_dict(series, index, columns, None)
