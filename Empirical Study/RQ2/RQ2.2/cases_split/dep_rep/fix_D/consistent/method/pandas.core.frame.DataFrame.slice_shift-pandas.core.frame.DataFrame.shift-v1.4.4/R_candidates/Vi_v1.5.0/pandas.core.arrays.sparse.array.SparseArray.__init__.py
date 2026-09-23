    def __init__(
        self,
        data,
        sparse_index=None,
        index=None,
        fill_value=None,
        kind: SparseIndexKind = "integer",
        dtype: Dtype | None = None,
        copy: bool = False,
    ) -> None:

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

        if index is not None:
            warnings.warn(
                "The index argument has been deprecated and will be "
                "removed in a future version. Use a function like np.full "
                "to construct an array with the desired repeats of the "
                "scalar value instead.\n\n",
                FutureWarning,
                stacklevel=find_stack_level(inspect.currentframe()),
            )

        if index is not None and not is_scalar(data):
            raise Exception("must only pass scalars with an index")

        if is_scalar(data):
            if index is not None and data is None:
                data = np.nan

            if index is not None:
                npoints = len(index)
            elif sparse_index is None:
                npoints = 1
            else:
                npoints = sparse_index.length

            data = construct_1d_arraylike_from_scalar(data, npoints, dtype=None)
            dtype = data.dtype

        if dtype is not None:
            dtype = pandas_dtype(dtype)

        # TODO: disentangle the fill_value dtype inference from
        # dtype inference
        if data is None:
            # TODO: What should the empty dtype be? Object or float?

            # error: Argument "dtype" to "array" has incompatible type
            # "Union[ExtensionDtype, dtype[Any], None]"; expected "Union[dtype[Any],
            # None, type, _SupportsDType, str, Union[Tuple[Any, int], Tuple[Any,
            # Union[int, Sequence[int]]], List[Any], _DTypeDict, Tuple[Any, Any]]]"
            data = np.array([], dtype=dtype)  # type: ignore[arg-type]

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
            # error: Argument "dtype" to "asarray" has incompatible type
            # "Union[ExtensionDtype, dtype[Any], Type[object], None]"; expected
            # "Union[dtype[Any], None, type, _SupportsDType, str, Union[Tuple[Any, int],
            # Tuple[Any, Union[int, Sequence[int]]], List[Any], _DTypeDict, Tuple[Any,
            # Any]]]"
            sparse_values = np.asarray(
                data.sp_values, dtype=dtype  # type: ignore[arg-type]
            )
        elif sparse_index is None:
            data = extract_array(data, extract_numpy=True)
            if not isinstance(data, np.ndarray):
                # EA
                if is_datetime64tz_dtype(data.dtype):
                    warnings.warn(
                        f"Creating SparseArray from {data.dtype} data "
                        "loses timezone information. Cast to object before "
                        "sparse to retain timezone information.",
                        UserWarning,
                        stacklevel=find_stack_level(inspect.currentframe()),
                    )
                    data = np.asarray(data, dtype="datetime64[ns]")
                    if fill_value is NaT:
                        fill_value = np.datetime64("NaT", "ns")
                data = np.asarray(data)
            sparse_values, sparse_index, fill_value = make_sparse(
                # error: Argument "dtype" to "make_sparse" has incompatible type
                # "Union[ExtensionDtype, dtype[Any], Type[object], None]"; expected
                # "Union[str, dtype[Any], None]"
                data,
                kind=kind,
                fill_value=fill_value,
                dtype=dtype,  # type: ignore[arg-type]
            )
        else:
            # error: Argument "dtype" to "asarray" has incompatible type
            # "Union[ExtensionDtype, dtype[Any], Type[object], None]"; expected
            # "Union[dtype[Any], None, type, _SupportsDType, str, Union[Tuple[Any, int],
            # Tuple[Any, Union[int, Sequence[int]]], List[Any], _DTypeDict, Tuple[Any,
            # Any]]]"
            sparse_values = np.asarray(data, dtype=dtype)  # type: ignore[arg-type]
            if len(sparse_values) != sparse_index.npoints:
                raise AssertionError(
                    f"Non array-like type {type(sparse_values)} must "
                    "have the same length as the index"
                )
        self._sparse_index = sparse_index
        self._sparse_values = sparse_values
        self._dtype = SparseDtype(sparse_values.dtype, fill_value)
