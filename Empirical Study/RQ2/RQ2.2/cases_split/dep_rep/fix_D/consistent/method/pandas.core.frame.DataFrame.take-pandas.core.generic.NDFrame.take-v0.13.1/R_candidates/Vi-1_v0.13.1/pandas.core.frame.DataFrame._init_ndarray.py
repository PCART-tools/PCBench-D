    def _init_ndarray(self, values, index, columns, dtype=None,
                      copy=False):
        if isinstance(values, Series):
            if columns is None:
                if values.name is not None:
                    columns = [values.name]
            if index is None:
                index = values.index
            else:
                values = values.reindex(index)

            # zero len case (GH #2234)
            if not len(values) and columns is not None and len(columns):
                values = np.empty((0, 1), dtype=object)

        values = _prep_ndarray(values, copy=copy)

        if dtype is not None:
            if values.dtype != dtype:
                try:
                    values = values.astype(dtype)
                except Exception as orig:
                    e = ValueError("failed to cast to '%s' (Exception was: %s)"
                                   % (dtype, orig))
                    raise_with_traceback(e)

        N, K = values.shape

        if index is None:
            index = _default_index(N)
        else:
            index = _ensure_index(index)

        if columns is None:
            columns = _default_index(K)
        else:
            columns = _ensure_index(columns)

        return create_block_manager_from_blocks([values.T], [columns, index])
