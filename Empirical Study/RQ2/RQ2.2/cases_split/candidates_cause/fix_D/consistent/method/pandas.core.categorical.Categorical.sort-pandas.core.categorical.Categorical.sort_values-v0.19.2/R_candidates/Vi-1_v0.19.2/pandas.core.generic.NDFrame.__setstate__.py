    def __setstate__(self, state):

        if isinstance(state, BlockManager):
            self._data = state
        elif isinstance(state, dict):
            typ = state.get('_typ')
            if typ is not None:

                # set in the order of internal names
                # to avoid definitional recursion
                # e.g. say fill_value needing _data to be
                # defined
                meta = set(self._internal_names + self._metadata)
                for k in list(meta):
                    if k in state:
                        v = state[k]
                        object.__setattr__(self, k, v)

                for k, v in state.items():
                    if k not in meta:
                        object.__setattr__(self, k, v)

            else:
                self._unpickle_series_compat(state)
        elif isinstance(state[0], dict):
            if len(state) == 5:
                self._unpickle_sparse_frame_compat(state)
            else:
                self._unpickle_frame_compat(state)
        elif len(state) == 4:
            self._unpickle_panel_compat(state)
        elif len(state) == 2:
            self._unpickle_series_compat(state)
        else:  # pragma: no cover
            # old pickling format, for compatibility
            self._unpickle_matrix_compat(state)

        self._item_cache = {}
