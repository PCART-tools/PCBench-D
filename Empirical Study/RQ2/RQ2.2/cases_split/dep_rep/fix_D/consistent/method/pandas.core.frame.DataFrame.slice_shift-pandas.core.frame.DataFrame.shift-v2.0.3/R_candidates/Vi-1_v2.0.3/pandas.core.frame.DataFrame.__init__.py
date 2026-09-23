    def __init__(
        self,
        data=None,
        index: Axes | None = None,
        columns: Axes | None = None,
        dtype: Dtype | None = None,
        copy: bool | None = None,
    ) -> None:
        if dtype is not None:
            dtype = self._validate_dtype(dtype)

        if isinstance(data, DataFrame):
            data = data._mgr
            if not copy:
                # if not copying data, ensure to still return a shallow copy
                # to avoid the result sharing the same Manager
                data = data.copy(deep=False)

        if isinstance(data, (BlockManager, ArrayManager)):
            if using_copy_on_write():
                data = data.copy(deep=False)
            # first check if a Manager is passed without any other arguments
            # -> use fastpath (without checking Manager type)
            if index is None and columns is None and dtype is None and not copy:
                # GH#33357 fastpath
                NDFrame.__init__(self, data)
                return

        manager = get_option("mode.data_manager")

        # GH47215
        if index is not None and isinstance(index, set):
            raise ValueError("index cannot be a set")
        if columns is not None and isinstance(columns, set):
            raise ValueError("columns cannot be a set")

        if copy is None:
            if isinstance(data, dict):
                # retain pre-GH#38939 default behavior
                copy = True
            elif (
                manager == "array"
                and isinstance(data, (np.ndarray, ExtensionArray))
                and data.ndim == 2
            ):
                # INFO(ArrayManager) by default copy the 2D input array to get
                # contiguous 1D arrays
                copy = True
            elif using_copy_on_write() and not isinstance(
                data, (Index, DataFrame, Series)
            ):
                copy = True
            else:
                copy = False

        if data is None:
            index = index if index is not None else default_index(0)
            columns = columns if columns is not None else default_index(0)
            dtype = dtype if dtype is not None else pandas_dtype(object)
            data = []

        if isinstance(data, (BlockManager, ArrayManager)):
            mgr = self._init_mgr(
                data, axes={"index": index, "columns": columns}, dtype=dtype, copy=copy
            )

        elif isinstance(data, dict):
            # GH#38939 de facto copy defaults to False only in non-dict cases
            mgr = dict_to_mgr(data, index, columns, dtype=dtype, copy=copy, typ=manager)
        elif isinstance(data, ma.MaskedArray):
            from numpy.ma import mrecords

            # masked recarray
            if isinstance(data, mrecords.MaskedRecords):
                raise TypeError(
                    "MaskedRecords are not supported. Pass "
                    "{name: data[name] for name in data.dtype.names} "
                    "instead"
                )

            # a masked array
            data = sanitize_masked_array(data)
            mgr = ndarray_to_mgr(
                data,
                index,
                columns,
                dtype=dtype,
                copy=copy,
                typ=manager,
            )

        elif isinstance(data, (np.ndarray, Series, Index, ExtensionArray)):
            if data.dtype.names:
                # i.e. numpy structured array
                data = cast(np.ndarray, data)
                mgr = rec_array_to_mgr(
                    data,
                    index,
                    columns,
                    dtype,
                    copy,
                    typ=manager,
                )
            elif getattr(data, "name", None) is not None:
                # i.e. Series/Index with non-None name
                _copy = copy if using_copy_on_write() else True
                mgr = dict_to_mgr(
                    # error: Item "ndarray" of "Union[ndarray, Series, Index]" has no
                    # attribute "name"
                    {data.name: data},  # type: ignore[union-attr]
                    index,
                    columns,
                    dtype=dtype,
                    typ=manager,
                    copy=_copy,
                )
            else:
                mgr = ndarray_to_mgr(
                    data,
                    index,
                    columns,
                    dtype=dtype,
                    copy=copy,
                    typ=manager,
                )

        # For data is list-like, or Iterable (will consume into list)
        elif is_list_like(data):
            if not isinstance(data, abc.Sequence):
                if hasattr(data, "__array__"):
                    # GH#44616 big perf improvement for e.g. pytorch tensor
                    data = np.asarray(data)
                else:
                    data = list(data)
            if len(data) > 0:
                if is_dataclass(data[0]):
                    data = dataclasses_to_dicts(data)
                if not isinstance(data, np.ndarray) and treat_as_nested(data):
                    # exclude ndarray as we may have cast it a few lines above
                    if columns is not None:
                        columns = ensure_index(columns)
                    arrays, columns, index = nested_data_to_arrays(
                        # error: Argument 3 to "nested_data_to_arrays" has incompatible
                        # type "Optional[Collection[Any]]"; expected "Optional[Index]"
                        data,
                        columns,
                        index,  # type: ignore[arg-type]
                        dtype,
                    )
                    mgr = arrays_to_mgr(
                        arrays,
                        columns,
                        index,
                        dtype=dtype,
                        typ=manager,
                    )
                else:
                    mgr = ndarray_to_mgr(
                        data,
                        index,
                        columns,
                        dtype=dtype,
                        copy=copy,
                        typ=manager,
                    )
            else:
                mgr = dict_to_mgr(
                    {},
                    index,
                    columns if columns is not None else default_index(0),
                    dtype=dtype,
                    typ=manager,
                )
        # For data is scalar
        else:
            if index is None or columns is None:
                raise ValueError("DataFrame constructor not properly called!")

            index = ensure_index(index)
            columns = ensure_index(columns)

            if not dtype:
                dtype, _ = infer_dtype_from_scalar(data, pandas_dtype=True)

            # For data is a scalar extension dtype
            if isinstance(dtype, ExtensionDtype):
                # TODO(EA2D): special case not needed with 2D EAs

                values = [
                    construct_1d_arraylike_from_scalar(data, len(index), dtype)
                    for _ in range(len(columns))
                ]
                mgr = arrays_to_mgr(values, columns, index, dtype=None, typ=manager)
            else:
                arr2d = construct_2d_arraylike_from_scalar(
                    data,
                    len(index),
                    len(columns),
                    dtype,
                    copy,
                )

                mgr = ndarray_to_mgr(
                    arr2d,
                    index,
                    columns,
                    dtype=arr2d.dtype,
                    copy=False,
                    typ=manager,
                )

        # ensure correct Manager type according to settings
        mgr = mgr_to_mgr(mgr, typ=manager)

        NDFrame.__init__(self, mgr)
