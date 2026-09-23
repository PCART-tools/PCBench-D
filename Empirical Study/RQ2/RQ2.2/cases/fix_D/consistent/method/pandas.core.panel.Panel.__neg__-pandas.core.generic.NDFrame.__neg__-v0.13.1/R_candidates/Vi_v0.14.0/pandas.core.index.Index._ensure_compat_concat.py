    @staticmethod
    def _ensure_compat_concat(indexes):
        from pandas.tseries.api import DatetimeIndex, PeriodIndex
        klasses = DatetimeIndex, PeriodIndex

        is_ts = [isinstance(idx, klasses) for idx in indexes]

        if any(is_ts) and not all(is_ts):
            return [_maybe_box(idx) for idx in indexes]

        return indexes
