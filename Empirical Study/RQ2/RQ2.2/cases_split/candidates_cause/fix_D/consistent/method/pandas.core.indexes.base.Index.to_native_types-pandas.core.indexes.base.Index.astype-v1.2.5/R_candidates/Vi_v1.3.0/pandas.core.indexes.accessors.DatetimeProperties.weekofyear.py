    @property
    def weekofyear(self):
        """
        The week ordinal of the year.

        .. deprecated:: 1.1.0

        Series.dt.weekofyear and Series.dt.week have been deprecated.
        Please use Series.dt.isocalendar().week instead.
        """
        warnings.warn(
            "Series.dt.weekofyear and Series.dt.week have been deprecated.  "
            "Please use Series.dt.isocalendar().week instead.",
            FutureWarning,
            stacklevel=2,
        )
        week_series = self.isocalendar().week
        week_series.name = self.name
        if week_series.hasnans:
            return week_series.astype("float64")
        return week_series.astype("int64")
