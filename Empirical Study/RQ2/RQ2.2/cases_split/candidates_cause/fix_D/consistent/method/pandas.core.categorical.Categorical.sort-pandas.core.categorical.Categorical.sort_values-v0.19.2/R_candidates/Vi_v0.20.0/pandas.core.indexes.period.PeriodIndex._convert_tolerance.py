    def _convert_tolerance(self, tolerance):
        tolerance = DatetimeIndexOpsMixin._convert_tolerance(self, tolerance)
        return self._maybe_convert_timedelta(tolerance)
