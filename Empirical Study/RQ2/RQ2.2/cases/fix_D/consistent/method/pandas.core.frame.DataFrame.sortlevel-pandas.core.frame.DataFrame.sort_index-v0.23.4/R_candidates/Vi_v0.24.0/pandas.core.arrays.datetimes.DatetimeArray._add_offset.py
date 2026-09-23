    def _add_offset(self, offset):
        assert not isinstance(offset, Tick)
        try:
            if self.tz is not None:
                values = self.tz_localize(None)
            else:
                values = self
            result = offset.apply_index(values)
            if self.tz is not None:
                result = result.tz_localize(self.tz)

        except NotImplementedError:
            warnings.warn("Non-vectorized DateOffset being applied to Series "
                          "or DatetimeIndex", PerformanceWarning)
            result = self.astype('O') + offset

        return type(self)._from_sequence(result, freq='infer')
