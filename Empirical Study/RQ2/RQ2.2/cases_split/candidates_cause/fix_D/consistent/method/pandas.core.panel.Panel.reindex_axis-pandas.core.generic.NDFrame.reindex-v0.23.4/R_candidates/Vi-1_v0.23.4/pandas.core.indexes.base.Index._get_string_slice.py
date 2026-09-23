    def _get_string_slice(self, key, use_lhs=True, use_rhs=True):
        # this is for partial string indexing,
        # overridden in DatetimeIndex, TimedeltaIndex and PeriodIndex
        raise NotImplementedError
