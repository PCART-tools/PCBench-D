    def _add_offset(self, offset):
        if self.ndim == 2:
            return self.ravel()._add_offset(offset).reshape(self.shape)

        assert not isinstance(offset, Tick)
        try:
            if self.tz is not None:
                values = self.tz_localize(None)
            else:
                values = self
            result = offset._apply_array(values)
            result = DatetimeArray._simple_new(result)
            result = result.tz_localize(self.tz)

        except NotImplementedError:
            warnings.warn(
                "Non-vectorized DateOffset being applied to Series or DatetimeIndex",
                PerformanceWarning,
            )
            result = self.astype("O") + offset
            if not len(self):
                # GH#30336 _from_sequence won't be able to infer self.tz
                return type(self)._from_sequence(result).tz_localize(self.tz)

        return type(self)._from_sequence(result)
