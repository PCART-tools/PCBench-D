    def get_value_maybe_box(self, series, key):
        if not isinstance(key, Timedelta):
            key = Timedelta(key)
        values = self._engine.get_value(com._values_from_object(series), key)
        return com._maybe_box(self, values, series, key)
