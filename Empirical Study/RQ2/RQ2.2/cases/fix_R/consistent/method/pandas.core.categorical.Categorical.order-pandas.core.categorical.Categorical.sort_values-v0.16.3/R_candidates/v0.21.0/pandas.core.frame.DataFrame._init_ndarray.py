    def _init_ndarray(self, values, index, columns, dtype=None, copy=False):
        # input must be a ndarray, list, Series, index

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

        # helper to create the axes as indexes
        def _get_axes(N, K, index=index, columns=columns):
            # return axes or defaults

            if index is None:
                index = _default_index(N)
            else:
                index = _ensure_index(index)

            if columns is None:
                columns = _default_index(K)
            else:
                columns = _ensure_index(columns)
            return index, columns

        # we could have a categorical type passed or coerced to 'category'
        # recast this to an _arrays_to_mgr
        if (is_categorical_dtype(getattr(values, 'dtype', None)) or
                is_categorical_dtype(dtype)):

            if not hasattr(values, 'dtype'):
                values = _prep_ndarray(values, copy=copy)
                values = values.ravel()
            elif copy:
                values = values.copy()

            index, columns = _get_axes(len(values), 1)
            return _arrays_to_mgr([values], columns, index, columns,
                                  dtype=dtype)
        elif is_datetimetz(values):
            return self._init_dict({0: values}, index, columns, dtype=dtype)

        # by definition an array here
        # the dtypes will be coerced to a single dtype
        values = _prep_ndarray(values, copy=copy)

        if dtype is not None:
            if not is_dtype_equal(values.dtype, dtype):
                try:
                    values = values.astype(dtype)
                except Exception as orig:
                    e = ValueError("failed to cast to '%s' (Exception was: %s)"
                                   % (dtype, orig))
                    raise_with_traceback(e)

        index, columns = _get_axes(*values.shape)
        values = values.T

        # if we don't have a dtype specified, then try to convert objects
        # on the entire block; this is to convert if we have datetimelike's
        # embedded in an object type
        if dtype is None and is_object_dtype(values):
            values = maybe_infer_to_datetimelike(values)

        return create_block_manager_from_blocks([values], [columns, index])
