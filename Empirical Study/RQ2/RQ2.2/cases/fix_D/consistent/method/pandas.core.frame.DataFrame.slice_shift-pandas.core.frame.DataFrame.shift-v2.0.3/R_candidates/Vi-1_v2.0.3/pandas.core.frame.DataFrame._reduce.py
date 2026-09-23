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

        def blk_func(values, axis: Axis = 1):
            if isinstance(values, ExtensionArray):
                if not is_1d_only_ea_dtype(values.dtype) and not isinstance(
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

        # Case with EAs see GH#35881
        df = self
        if numeric_only:
            df = _get_data()
        if axis is None:
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
            df = df.T

        # After possibly _get_data and transposing, we are now in the
        #  simple case where we can use BlockManager.reduce
        res = df._mgr.reduce(blk_func)
        out = df._constructor(res).iloc[0]
        if out_dtype is not None:
            out = out.astype(out_dtype)
        elif (df._mgr.get_dtypes() == object).any():
            out = out.astype(object)
        elif len(self) == 0 and name in ("sum", "prod"):
            # Even if we are object dtype, follow numpy and return
            #  float64, see test_apply_funcs_over_empty
            out = out.astype(np.float64)

        return out
