    def get_value_maybe_box(self, series, key):
        # needed to localize naive datetimes
        if self.tz is not None:
            key = Timestamp(key, tz=self.tz)
        elif not isinstance(key, Timestamp):
            key = Timestamp(key)
        values = self._engine.get_value(_values_from_object(series),
                                        key, tz=self.tz)
        return _maybe_box(self, values, series, key)
