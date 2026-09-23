    @property
    def weekofyear(self):
        """
        The week ordinal of the year.

        .. deprecated:: 1.1.0

        weekofyear and week have been deprecated.
        Please use DatetimeIndex.isocalendar().week instead.
        """
        warnings.warn(
            "weekofyear and week have been deprecated, please use "
            "DatetimeIndex.isocalendar().week instead, which returns "
            "a Series.  To exactly reproduce the behavior of week and "
            "weekofyear and return an Index, you may call "
            "pd.Int64Index(idx.isocalendar().week)",
            FutureWarning,
            stacklevel=3,
        )
        week_series = self.isocalendar().week
        if week_series.hasnans:
            return week_series.to_numpy(dtype="float64", na_value=np.nan)
        return week_series.to_numpy(dtype="int64")
