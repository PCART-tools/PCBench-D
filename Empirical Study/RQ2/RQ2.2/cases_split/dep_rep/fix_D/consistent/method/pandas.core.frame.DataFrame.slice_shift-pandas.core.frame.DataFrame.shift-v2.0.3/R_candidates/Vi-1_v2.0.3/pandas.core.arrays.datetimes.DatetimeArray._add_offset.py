    def _add_offset(self, offset) -> DatetimeArray:
        assert not isinstance(offset, Tick)

        if self.tz is not None:
            values = self.tz_localize(None)
        else:
            values = self

        try:
            result = offset._apply_array(values).view(values.dtype)
        except NotImplementedError:
            warnings.warn(
                "Non-vectorized DateOffset being applied to Series or DatetimeIndex.",
                PerformanceWarning,
                stacklevel=find_stack_level(),
            )
            result = self.astype("O") + offset
            result = type(self)._from_sequence(result).as_unit(self.unit)
            if not len(self):
                # GH#30336 _from_sequence won't be able to infer self.tz
                return result.tz_localize(self.tz)

        else:
            result = DatetimeArray._simple_new(result, dtype=result.dtype)
            if self.tz is not None:
                result = result.tz_localize(self.tz)

        return result
