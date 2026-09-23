    @final
    @Substitution(name="groupby")
    @Appender(_common_see_also)
    def cummin(
        self, axis: AxisInt = 0, numeric_only: bool = False, **kwargs
    ) -> NDFrameT:
        """
        Cumulative min for each group.

        Returns
        -------
        Series or DataFrame
        """
        skipna = kwargs.get("skipna", True)
        if axis != 0:
            f = lambda x: np.minimum.accumulate(x, axis)
            obj = self._selected_obj
            if numeric_only:
                obj = obj._get_numeric_data()
            return self._python_apply_general(f, obj, is_transform=True)

        return self._cython_transform(
            "cummin", numeric_only=numeric_only, skipna=skipna
        )
