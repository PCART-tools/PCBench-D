    def _get_time_micros(self):
        utc = _utc()
        values = self.asi8
        if self.tz is not None and self.tz is not utc:
            values = self._local_timestamps()
        return libts.get_time_micros(values)
