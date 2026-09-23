    @Appender(DataFrame.idxmin.__doc__)
    def idxmin(self, axis=0, skipna: bool = True):
        axis = DataFrame._get_axis_number(axis)
        numeric_only = None if axis == 0 else False

        def func(df):
            # NB: here we use numeric_only=None, in DataFrame it is False GH#38217
            res = df._reduce(
                nanops.nanargmin,
                "argmin",
                axis=axis,
                skipna=skipna,
                numeric_only=numeric_only,
            )
            indices = res._values
            index = df._get_axis(axis)
            result = [index[i] if i >= 0 else np.nan for i in indices]
            return df._constructor_sliced(result, index=res.index)

        func.__name__ = "idxmin"
        return self._python_apply_general(func, self._obj_with_exclusions)
