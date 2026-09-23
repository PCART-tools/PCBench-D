    def get_value(self, series, key):
        """
        Fast lookup of value from 1-dimensional ndarray. Only use this if you
        know what you're doing
        """

        if _is_convertible_to_td(key):
            key = Timedelta(key)
            return self.get_value_maybe_box(series, key)

        try:
            value = Index.get_value(self, series, key)
        except KeyError:
            try:
                loc = self._get_string_slice(key)
                return series[loc]
            except (TypeError, ValueError, KeyError):
                pass

            try:
                return self.get_value_maybe_box(series, key)
            except (TypeError, ValueError, KeyError):
                raise KeyError(key)
        else:
            return com.maybe_box(self, value, series, key)
