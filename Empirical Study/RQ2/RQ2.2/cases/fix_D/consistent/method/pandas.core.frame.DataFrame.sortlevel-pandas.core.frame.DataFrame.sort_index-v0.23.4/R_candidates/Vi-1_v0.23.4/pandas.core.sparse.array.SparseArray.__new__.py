    def __new__(cls, data, sparse_index=None, index=None, kind='integer',
                fill_value=None, dtype=None, copy=False):

        if index is not None:
            if data is None:
                data = np.nan
            if not is_scalar(data):
                raise Exception("must only pass scalars with an index ")
            dtype = infer_dtype_from_scalar(data)[0]
            data = construct_1d_arraylike_from_scalar(
                data, len(index), dtype)

        if isinstance(data, ABCSparseSeries):
            data = data.values
        is_sparse_array = isinstance(data, SparseArray)

        if dtype is not None:
            dtype = np.dtype(dtype)

        if is_sparse_array:
            sparse_index = data.sp_index
            values = data.sp_values
            fill_value = data.fill_value
        else:
            # array-like
            if sparse_index is None:
                if dtype is not None:
                    data = np.asarray(data, dtype=dtype)
                res = make_sparse(data, kind=kind, fill_value=fill_value)
                values, sparse_index, fill_value = res
            else:
                values = _sanitize_values(data)
                if len(values) != sparse_index.npoints:
                    raise AssertionError("Non array-like type {type} must "
                                         "have the same length as the index"
                                         .format(type=type(values)))
        # Create array, do *not* copy data by default
        if copy:
            subarr = np.array(values, dtype=dtype, copy=True)
        else:
            subarr = np.asarray(values, dtype=dtype)
        # Change the class of the array to be the subclass type.
        return cls._simple_new(subarr, sparse_index, fill_value)
