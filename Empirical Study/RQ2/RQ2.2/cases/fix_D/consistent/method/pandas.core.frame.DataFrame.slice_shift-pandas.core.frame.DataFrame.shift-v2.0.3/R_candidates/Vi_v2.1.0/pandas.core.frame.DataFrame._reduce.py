    def _reduce(
        self,
        op,
        name: str,
        *,
        axis: Axis = 0,
        skipna: bool = True,
        numeric_only: bool = False,
        filter_type=None,
        **kwds,
    ):
        assert filter_type is None or filter_type == "bool", filter_type
        out_dtype = "bool" if filter_type == "bool" else None

        if axis is not None:
            axis = self._get_axis_number(axis)

        def func(values: np.ndarray):
            # We only use this in the case that operates on self.values
            return op(values, axis=axis, skipna=skipna, **kwds)

        dtype_has_keepdims: dict[ExtensionDtype, bool] = {}

        def blk_func(values, axis: Axis = 1):
            if isinstance(values, ExtensionArray):
                if not is_1d_only_ea_dtype(values.dtype) and not isinstance(
                    self._mgr, ArrayManager
                ):
                    return values._reduce(name, axis=1, skipna=skipna, **kwds)
                has_keepdims = dtype_has_keepdims.get(values.dtype)
                if has_keepdims is None:
                    sign = signature(values._reduce)
                    has_keepdims = "keepdims" in sign.parameters
                    dtype_has_keepdims[values.dtype] = has_keepdims
                if has_keepdims:
                    return values._reduce(name, skipna=skipna, keepdims=True, **kwds)
                else:
                    warnings.warn(
                        f"{type(values)}._reduce will require a `keepdims` parameter "
                        "in the future",
                        FutureWarning,
                        stacklevel=find_stack_level(),
                    )
                    result = values._reduce(name, skipna=skipna, **kwds)
                    return np.array([result])
            else:
                return op(values, axis=axis, skipna=skipna, **kwds)

        def _get_data() -> DataFrame:
            if filter_type is None:
                data = self._get_numeric_data()
            else:
                # GH#25101, GH#24434
                assert filter_type == "bool"
                data = self._get_bool_data()
            return data

        # Case with EAs see GH#35881
        df = self
        if numeric_only:
            df = _get_data()
        if axis is None:
            dtype = find_common_type([arr.dtype for arr in df._mgr.arrays])
            if isinstance(dtype, ExtensionDtype):
                df = df.astype(dtype, copy=False)
                arr = concat_compat(list(df._iter_column_arrays()))
                return arr._reduce(name, skipna=skipna, keepdims=False, **kwds)
            return func(df.values)
        elif axis == 1:
            if len(df.index) == 0:
                # Taking a transpose would result in no columns, losing the dtype.
                # In the empty case, reducing along axis 0 or 1 gives the same
                # result dtype, so reduce with axis=0 and ignore values
                result = df._reduce(
                    op,
                    name,
                    axis=0,
                    skipna=skipna,
                    numeric_only=False,
                    filter_type=filter_type,
                    **kwds,
                ).iloc[:0]
                result.index = df.index
                return result

            # kurtosis excluded since groupby does not implement it
            if df.shape[1] and name != "kurt":
                dtype = find_common_type([arr.dtype for arr in df._mgr.arrays])
                if isinstance(dtype, ExtensionDtype):
                    # GH 54341: fastpath for EA-backed axis=1 reductions
                    # This flattens the frame into a single 1D array while keeping
                    # track of the row and column indices of the original frame. Once
                    # flattened, grouping by the row indices and aggregating should
                    # be equivalent to transposing the original frame and aggregating
                    # with axis=0.
                    name = {"argmax": "idxmax", "argmin": "idxmin"}.get(name, name)
                    df = df.astype(dtype, copy=False)
                    arr = concat_compat(list(df._iter_column_arrays()))
                    nrows, ncols = df.shape
                    row_index = np.tile(np.arange(nrows), ncols)
                    col_index = np.repeat(np.arange(ncols), nrows)
                    ser = Series(arr, index=col_index, copy=False)
                    result = ser.groupby(row_index).agg(name, **kwds)
                    result.index = df.index
                    if not skipna and name not in ("any", "all"):
                        mask = df.isna().to_numpy(dtype=np.bool_).any(axis=1)
                        other = -1 if name in ("idxmax", "idxmin") else lib.no_default
                        result = result.mask(mask, other)
                    return result

            df = df.T

        # After possibly _get_data and transposing, we are now in the
        #  simple case where we can use BlockManager.reduce
        res = df._mgr.reduce(blk_func)
        out = df._constructor_from_mgr(res, axes=res.axes).iloc[0]
        if out_dtype is not None and out.dtype != "boolean":
            out = out.astype(out_dtype)
        elif (df._mgr.get_dtypes() == object).any() and name not in ["any", "all"]:
            out = out.astype(object)
        elif len(self) == 0 and out.dtype == object and name in ("sum", "prod"):
            # Even if we are object dtype, follow numpy and return
            #  float64, see test_apply_funcs_over_empty
            out = out.astype(np.float64)

        return out
