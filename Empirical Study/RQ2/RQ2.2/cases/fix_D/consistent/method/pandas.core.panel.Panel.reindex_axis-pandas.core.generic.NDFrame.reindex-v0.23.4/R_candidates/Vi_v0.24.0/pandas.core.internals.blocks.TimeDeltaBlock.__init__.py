    def __init__(self, values, placement, ndim=None):
        if values.dtype != _TD_DTYPE:
            values = conversion.ensure_timedelta64ns(values)
        if isinstance(values, TimedeltaArray):
            values = values._data
        assert isinstance(values, np.ndarray), type(values)
        super(TimeDeltaBlock, self).__init__(values,
                                             placement=placement, ndim=ndim)
