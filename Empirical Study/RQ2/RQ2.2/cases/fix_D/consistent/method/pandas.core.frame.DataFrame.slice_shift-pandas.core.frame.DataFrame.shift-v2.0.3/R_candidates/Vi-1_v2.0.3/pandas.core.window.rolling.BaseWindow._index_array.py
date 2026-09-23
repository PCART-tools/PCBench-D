    @property
    def _index_array(self):
        # TODO: why do we get here with e.g. MultiIndex?
        if needs_i8_conversion(self._on.dtype):
            idx = cast("PeriodIndex | DatetimeIndex | TimedeltaIndex", self._on)
            return idx.asi8
        return None
