    def __init__(
        self,
        data,
        sparse_index=None,
        index=None,
        fill_value=None,
        kind="integer",
        dtype=None,
        copy=False,
    ):

        if fill_value is None and isinstance(dtype, SparseDtype):
            fill_value = dtype.fill_value

        if isinstance(data, type(self)):
            # disable normal inference on dtype, sparse_index, & fill_value
            if sparse_index is None:
                sparse_index = data.sp_index
            if fill_value is None:
                fill_value = data.fill_value
            if dtype is None:
                dtype = data.dtype
            # TODO: make kind=None, and use data.kind?
            data = data.sp_values

        # Handle use-provided dtype
        if isinstance(dtype, str):
            # Two options: dtype='int', regular numpy dtype
            # or dtype='Sparse[int]', a sparse dtype
            try:
                dtype = SparseDtype.construct_from_string(dtype)
            except TypeError:
                dtype = pandas_dtype(dtype)

        if isinstance(dtype, SparseDtype):
            if fill_value is None:
                fill_value = dtype.fill_value
            dtype = dtype.subtype

        if index is not None and not is_scalar(data):
            raise Exception("must only pass scalars with an index")

        if is_scalar(data):
            if index is not None:
                if data is None:
                    data = np.nan

            if index is not None:
                npoints = len(index)
            elif sparse_index is None:
                npoints = 1
            else:
                npoints = sparse_index.length

            dtype = infer_dtype_from_scalar(data)[0]
            data = construct_1d_arraylike_from_scalar(data, npoints, dtype)

        if dtype is not None:
            dtype = pandas_dtype(dtype)

        # TODO: disentangle the fill_value dtype inference from
        # dtype inference
        if data is None:
            # TODO: What should the empty dtype be? Object or float?
            data = np.array([], dtype=dtype)

        if not is_array_like(data):
            try:
                # probably shared code in sanitize_series

                data = sanitize_array(data, index=None)
            except ValueError:
                # NumPy may raise a ValueError on data like [1, []]
                # we retry with object dtype here.
                if dtype is None:
                    dtype = object
                    data = np.atleast_1d(np.asarray(data, dtype=dtype))
                else:
                    raise

        if copy:
            # TODO: avoid double copy when dtype forces cast.
            data = data.copy()

        if fill_value is None:
            fill_value_dtype = data.dtype if dtype is None else dtype
            if fill_value_dtype is None:
                fill_value = np.nan
            else:
                fill_value = na_value_for_dtype(fill_value_dtype)

        if isinstance(data, type(self)) and sparse_index is None:
            sparse_index = data._sparse_index
            sparse_values = np.asarray(data.sp_values, dtype=dtype)
        elif sparse_index is None:
            data = extract_array(data, extract_numpy=True)
            if not isinstance(data, np.ndarray):
                # EA
                if is_datetime64tz_dtype(data.dtype):
                    warnings.warn(
                        f"Creating SparseArray from {data.dtype} data "
                        "loses timezone information.  Cast to object before "
                        "sparse to retain timezone information.",
                        UserWarning,
                        stacklevel=2,
                    )
                    data = np.asarray(data, dtype="datetime64[ns]")
                data = np.asarray(data)
            sparse_values, sparse_index, fill_value = make_sparse(
                data, kind=kind, fill_value=fill_value, dtype=dtype
            )
        else:
            sparse_values = np.asarray(data, dtype=dtype)
            if len(sparse_values) != sparse_index.npoints:
                raise AssertionError(
                    f"Non array-like type {type(sparse_values)} must "
                    "have the same length as the index"
                )
        self._sparse_index = sparse_index
        self._sparse_values = sparse_values
        self._dtype = SparseDtype(sparse_values.dtype, fill_value)
