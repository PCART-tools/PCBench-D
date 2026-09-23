    @final
    @Substitution(name="groupby")
    @Appender(_common_see_also)
    def diff(self, periods: int = 1, axis: int = 0) -> NDFrameT:
        """
        First discrete difference of element.

        Calculates the difference of each element compared with another
        element in the group (default is element in previous row).

        Parameters
        ----------
        periods : int, default 1
            Periods to shift for calculating difference, accepts negative values.
        axis : axis to shift, default 0
            Take difference over rows (0) or columns (1).

        Returns
        -------
        Series or DataFrame
            First differences.
        """
        if axis != 0:
            return self.apply(lambda x: x.diff(periods=periods, axis=axis))

        obj = self._obj_with_exclusions
        shifted = self.shift(periods=periods, axis=axis)

        # GH45562 - to retain existing behavior and match behavior of Series.diff(),
        # int8 and int16 are coerced to float32 rather than float64.
        dtypes_to_f32 = ["int8", "int16"]
        if obj.ndim == 1:
            if obj.dtype in dtypes_to_f32:
                shifted = shifted.astype("float32")
        else:
            to_coerce = [c for c, dtype in obj.dtypes.items() if dtype in dtypes_to_f32]
            if len(to_coerce):
                shifted = shifted.astype({c: "float32" for c in to_coerce})

        return obj - shifted
