    @Substitution(name="groupby")
    @Appender(_common_see_also)
    def pct_change(self, periods=1, fill_method="pad", limit=None, freq=None, axis=0):
        """
        Calculate pct_change of each value to previous entry in group.

        Returns
        -------
        Series or DataFrame
            Percentage changes within each group.
        """
        if freq is not None or axis != 0:
            return self.apply(
                lambda x: x.pct_change(
                    periods=periods,
                    fill_method=fill_method,
                    limit=limit,
                    freq=freq,
                    axis=axis,
                )
            )
        if fill_method is None:  # GH30463
            fill_method = "pad"
            limit = 0
        filled = getattr(self, fill_method)(limit=limit)
        fill_grp = filled.groupby(self.grouper.codes)
        shifted = fill_grp.shift(periods=periods, freq=freq)
        return (filled / shifted) - 1
