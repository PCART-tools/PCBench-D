    def _maybe_convert_datelike_array(self):
        """Maybe convert to a datelike array."""
        pa_type = self._pa_array.type
        if pa.types.is_timestamp(pa_type):
            return self._to_datetimearray()
        elif pa.types.is_duration(pa_type):
            return self._to_timedeltaarray()
        return self
