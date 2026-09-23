    @cache_readonly
    def dt(self):
        from pandas.tseries.common import maybe_to_datetimelike
        try:
            return maybe_to_datetimelike(self)
        except (Exception):
            raise TypeError("Can only use .dt accessor with datetimelike values")
