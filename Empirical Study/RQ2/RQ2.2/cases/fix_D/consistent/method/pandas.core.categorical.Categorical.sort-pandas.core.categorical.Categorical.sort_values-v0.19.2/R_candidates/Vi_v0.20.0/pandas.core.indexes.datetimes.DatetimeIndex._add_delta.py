    def _add_delta(self, delta):
        from pandas import TimedeltaIndex
        name = self.name

        if isinstance(delta, (Tick, timedelta, np.timedelta64)):
            new_values = self._add_delta_td(delta)
        elif isinstance(delta, TimedeltaIndex):
            new_values = self._add_delta_tdi(delta)
            # update name when delta is Index
            name = com._maybe_match_name(self, delta)
        elif isinstance(delta, DateOffset):
            new_values = self._add_offset(delta).asi8
        else:
            new_values = self.astype('O') + delta

        tz = 'UTC' if self.tz is not None else None
        result = DatetimeIndex(new_values, tz=tz, name=name, freq='infer')
        utc = _utc()
        if self.tz is not None and self.tz is not utc:
            result = result.tz_convert(self.tz)
        return result
