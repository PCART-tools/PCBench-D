    @final
    @Substitution(name="groupby")
    @Appender(_common_see_also)
    def cumsum(self, axis: Axis = 0, *args, **kwargs) -> NDFrameT:
        """
        Cumulative sum for each group.

        Returns
        -------
        Series or DataFrame
        """
        nv.validate_groupby_func("cumsum", args, kwargs, ["numeric_only", "skipna"])
        if axis != 0:
            f = lambda x: x.cumsum(axis=axis, **kwargs)
            return self._python_apply_general(f, self._selected_obj, is_transform=True)

        return self._cython_transform("cumsum", **kwargs)
