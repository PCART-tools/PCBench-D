    @final
    @Substitution(name="groupby")
    @Appender(_common_see_also)
    def cumprod(self, axis=0, *args, **kwargs) -> NDFrameT:
        """
        Cumulative product for each group.

        Returns
        -------
        Series or DataFrame
        """
        nv.validate_groupby_func("cumprod", args, kwargs, ["numeric_only", "skipna"])
        if axis != 0:
            f = lambda x: x.cumprod(axis=axis, **kwargs)
            return self._python_apply_general(f, self._selected_obj, is_transform=True)

        return self._cython_transform("cumprod", **kwargs)
