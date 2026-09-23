    @Substitution(name="groupby")
    @Appender(_common_see_also)
    def cumprod(self, axis=0, *args, **kwargs):
        """
        Cumulative product for each group.

        Returns
        -------
        Series or DataFrame
        """
        nv.validate_groupby_func("cumprod", args, kwargs, ["numeric_only", "skipna"])
        if axis != 0:
            return self.apply(lambda x: x.cumprod(axis=axis, **kwargs))

        return self._cython_transform("cumprod", **kwargs)
