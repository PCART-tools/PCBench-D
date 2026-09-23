    def _add_offset(self, offset):
        try:
            if self.tz is not None:
                values = self.tz_localize(None)
            else:
                values = self
            result = offset.apply_index(values)
            if self.tz is not None:
                result = result.tz_localize(self.tz)
            return result

        except NotImplementedError:
            warnings.warn("Non-vectorized DateOffset being applied to Series "
                          "or DatetimeIndex", PerformanceWarning)
            return self.astype('O') + offset
