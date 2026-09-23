    @final
    @Substitution(name="groupby")
    @Appender(_common_see_also)
    def cummax(self, axis=0, **kwargs):
        """
        Cumulative max for each group.

        Returns
        -------
        Series or DataFrame
        """
        skipna = kwargs.get("skipna", True)
        if axis != 0:
            return self.apply(lambda x: np.maximum.accumulate(x, axis))

        return self._cython_transform("cummax", numeric_only=False, skipna=skipna)
