    def _reduce(
        self,
        op,
        name: str,
        *,
        axis: Axis = 0,
        skipna: bool = True,
        numeric_only: bool | None = None,
        filter_type=None,
        **kwds,
    ):

        assert filter_type is None or filter_type == "bool", filter_type
        out_dtype = "bool" if filter_type == "bool" else None

        if numeric_only is None and name in ["mean", "median"]:
            own_dtypes = [arr.dtype for arr in self._mgr.arrays]

            dtype_is_dt = np.array(
                [is_datetime64_any_dtype(dtype) for dtype in own_dtypes],
                dtype=bool,
            )
            if dtype_is_dt.any():
                warnings.warn(
                    "DataFrame.mean and DataFrame.median with numeric_only=None "
                    "will include datetime64 and datetime64tz columns in a "
                    "future version.",
                    FutureWarning,
                    stacklevel=find_stack_level(),
                )
                # Non-copy equivalent to
                #  dt64_cols = self.dtypes.apply(is_datetime64_any_dtype)
                #  cols = self.columns[~dt64_cols]
                #  self = self[cols]
                predicate = lambda x: not is_datetime64_any_dtype(x.dtype)
                mgr = self._mgr._get_data_subset(predicate)
                self = type(self)(mgr)

        # TODO: Make other agg func handle axis=None properly GH#21597
        axis = self._get_axis_number(axis)
        labels = self._get_agg_axis(axis)
        assert axis in [0, 1]

        def func(values: np.ndarray):
            # We only use this in the case that operates on self.values
            return op(values, axis=axis, skipna=skipna, **kwds)

        def blk_func(values, axis=1):
            if isinstance(values, ExtensionArray):
                if not is_1d_only_ea_obj(values) and not isinstance(
                    self._mgr, ArrayManager
                ):
                    return values._reduce(name, axis=1, skipna=skipna, **kwds)
                return values._reduce(name, skipna=skipna, **kwds)
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

        if numeric_only is not None or axis == 0:
            # For numeric_only non-None and axis non-None, we know
            #  which blocks to use and no try/except is needed.
            #  For numeric_only=None only the case with axis==0 and no object
            #  dtypes are unambiguous can be handled with BlockManager.reduce
            # Case with EAs see GH#35881
            df = self
            if numeric_only is True:
                df = _get_data()
            if axis == 1:
                df = df.T
                axis = 0

            ignore_failures = numeric_only is None

            # After possibly _get_data and transposing, we are now in the
            #  simple case where we can use BlockManager.reduce
            res, _ = df._mgr.reduce(blk_func, ignore_failures=ignore_failures)
            out = df._constructor(res).iloc[0]
            if out_dtype is not None:
                out = out.astype(out_dtype)
            if axis == 0 and len(self) == 0 and name in ["sum", "prod"]:
                # Even if we are object dtype, follow numpy and return
                #  float64, see test_apply_funcs_over_empty
                out = out.astype(np.float64)

            if numeric_only is None and out.shape[0] != df.shape[1]:
                # columns have been dropped GH#41480
                arg_name = "numeric_only"
                if name in ["all", "any"]:
                    arg_name = "bool_only"
                warnings.warn(
                    "Dropping of nuisance columns in DataFrame reductions "
                    f"(with '{arg_name}=None') is deprecated; in a future "
                    "version this will raise TypeError.  Select only valid "
                    "columns before calling the reduction.",
                    FutureWarning,
                    stacklevel=find_stack_level(),
                )

            return out

        assert numeric_only is None

        data = self
        values = data.values

        try:
            result = func(values)

        except TypeError:
            # e.g. in nanops trying to convert strs to float

            data = _get_data()
            labels = data._get_agg_axis(axis)

            values = data.values
            with np.errstate(all="ignore"):
                result = func(values)

            # columns have been dropped GH#41480
            arg_name = "numeric_only"
            if name in ["all", "any"]:
                arg_name = "bool_only"
            warnings.warn(
                "Dropping of nuisance columns in DataFrame reductions "
                f"(with '{arg_name}=None') is deprecated; in a future "
                "version this will raise TypeError.  Select only valid "
                "columns before calling the reduction.",
                FutureWarning,
                stacklevel=find_stack_level(),
            )

        if hasattr(result, "dtype"):
            if filter_type == "bool" and notna(result).all():
                result = result.astype(np.bool_)
            elif filter_type is None and is_object_dtype(result.dtype):
                try:
                    result = result.astype(np.float64)
                except (ValueError, TypeError):
                    # try to coerce to the original dtypes item by item if we can
                    pass

        result = self._constructor_sliced(result, index=labels)
        return result
