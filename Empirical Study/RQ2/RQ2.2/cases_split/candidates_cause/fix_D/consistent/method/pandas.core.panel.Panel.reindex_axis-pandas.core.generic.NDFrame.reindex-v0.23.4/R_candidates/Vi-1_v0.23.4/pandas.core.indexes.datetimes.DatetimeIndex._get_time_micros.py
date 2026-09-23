    def _get_time_micros(self):
        values = self.asi8
        if self.tz is not None and self.tz is not utc:
            values = self._local_timestamps()
        return fields.get_time_micros(values)
