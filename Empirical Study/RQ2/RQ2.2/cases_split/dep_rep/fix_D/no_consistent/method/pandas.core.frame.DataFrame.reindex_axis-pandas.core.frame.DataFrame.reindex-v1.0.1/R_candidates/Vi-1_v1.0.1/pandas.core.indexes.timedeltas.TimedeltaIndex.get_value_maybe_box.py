    def get_value_maybe_box(self, series, key: Timedelta):
        values = self._engine.get_value(com.values_from_object(series), key)
        return com.maybe_box(self, values, series, key)
