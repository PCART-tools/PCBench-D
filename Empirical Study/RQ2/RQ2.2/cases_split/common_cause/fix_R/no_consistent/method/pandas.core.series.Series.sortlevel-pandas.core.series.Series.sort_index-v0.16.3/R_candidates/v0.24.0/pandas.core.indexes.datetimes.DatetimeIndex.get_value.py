    def get_value(self, series, key):
        """
        Fast lookup of value from 1-dimensional ndarray. Only use this if you
        know what you're doing
        """

        if isinstance(key, datetime):

            # needed to localize naive datetimes
            if self.tz is not None:
                if key.tzinfo is not None:
                    key = Timestamp(key).tz_convert(self.tz)
                else:
                    key = Timestamp(key).tz_localize(self.tz)

            return self.get_value_maybe_box(series, key)

        if isinstance(key, time):
            locs = self.indexer_at_time(key)
            return series.take(locs)

        try:
            return com.maybe_box(self, Index.get_value(self, series, key),
                                 series, key)
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
