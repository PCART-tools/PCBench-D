    def get_value_maybe_box(self, series, key):
        # needed to localize naive datetimes
        if self.tz is not None:
            key = Timestamp(key)
            if key.tzinfo is not None:
                key = key.tz_convert(self.tz)
            else:
                key = key.tz_localize(self.tz)
        elif not isinstance(key, Timestamp):
            key = Timestamp(key)
        values = self._engine.get_value(com.values_from_object(series), key, tz=self.tz)
        return com.maybe_box(self, values, series, key)
