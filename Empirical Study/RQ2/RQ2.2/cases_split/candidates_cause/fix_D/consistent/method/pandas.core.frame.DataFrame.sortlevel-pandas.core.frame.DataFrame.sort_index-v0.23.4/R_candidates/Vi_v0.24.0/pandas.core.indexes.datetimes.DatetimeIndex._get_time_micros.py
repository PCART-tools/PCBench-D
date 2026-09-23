    def _get_time_micros(self):
        values = self.asi8
        if self.tz is not None and not timezones.is_utc(self.tz):
            values = self._data._local_timestamps()
        return fields.get_time_micros(values)
