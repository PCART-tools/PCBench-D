def _maybe_box(idx):
    from pandas.tseries.api import DatetimeIndex, PeriodIndex, TimedeltaIndex
    klasses = DatetimeIndex, PeriodIndex, TimedeltaIndex

    if isinstance(idx, klasses):
        return idx.asobject
    return idx
