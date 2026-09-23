    @doc(
        _shared_docs["idxmax"],
        numeric_only_default="True for axis=0, False for axis=1",
    )
    def idxmax(
        self,
        axis=0,
        skipna: bool = True,
        numeric_only: bool | lib.NoDefault = lib.no_default,
    ) -> DataFrame:
        axis = DataFrame._get_axis_number(axis)
        if numeric_only is lib.no_default:
            # Cannot use self._resolve_numeric_only; we must pass None to
            # DataFrame.idxmax for backwards compatibility
            numeric_only_arg = None if axis == 0 else False
        else:
            numeric_only_arg = numeric_only

        def func(df):
            with warnings.catch_warnings():
                # Suppress numeric_only warnings here, will warn below
                warnings.filterwarnings("ignore", ".*numeric_only in DataFrame.argmax")
                res = df._reduce(
                    nanops.nanargmax,
                    "argmax",
                    axis=axis,
                    skipna=skipna,
                    numeric_only=numeric_only_arg,
                )
                indices = res._values
                index = df._get_axis(axis)
                result = [index[i] if i >= 0 else np.nan for i in indices]
                return df._constructor_sliced(result, index=res.index)

        func.__name__ = "idxmax"
        result = self._python_apply_general(
            func, self._obj_with_exclusions, not_indexed_same=True
        )
        self._maybe_warn_numeric_only_depr("idxmax", result, numeric_only)
        return result
