    def get_value(self, series, key):
        """ we always want to get an index value, never a value """
        if not is_scalar(key):
            raise InvalidIndexError

        k = com._values_from_object(key)
        loc = self.get_loc(k)
        new_values = com._values_from_object(series)[loc]

        return new_values
