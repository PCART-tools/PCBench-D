    @Substitution(name="groupby")
    @Appender(_common_see_also)
    def cummin(self, axis=0, **kwargs):
        """
        Cumulative min for each group.

        Returns
        -------
        Series or DataFrame
        """
        if axis != 0:
            return self.apply(lambda x: np.minimum.accumulate(x, axis))

        return self._cython_transform("cummin", numeric_only=False)
