    @final
    @Substitution(name="groupby")
    @Appender(_common_see_also)
    def cummin(self, axis=0, numeric_only=False, **kwargs) -> NDFrameT:
        """
        Cumulative min for each group.

        Returns
        -------
        Series or DataFrame
        """
        skipna = kwargs.get("skipna", True)
        if axis != 0:
            f = lambda x: np.minimum.accumulate(x, axis)
            numeric_only_bool = self._resolve_numeric_only("cummax", numeric_only, axis)
            obj = self._selected_obj
            if numeric_only_bool:
                obj = obj._get_numeric_data()
            return self._python_apply_general(f, obj, is_transform=True)

        return self._cython_transform(
            "cummin", numeric_only=numeric_only, skipna=skipna
        )
