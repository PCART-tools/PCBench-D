    def get_value(self, series, key):
        """ we always want to get an index value, never a value """
        if not np.isscalar(key):
            raise InvalidIndexError

        from pandas.core.indexing import _maybe_droplevels
        from pandas.core.series import Series

        k = _values_from_object(key)
        loc = self.get_loc(k)
        new_values = series.values[loc]
        if np.isscalar(new_values):
            return new_values

        new_index = self[loc]
        new_index = _maybe_droplevels(new_index, k)
        return Series(new_values, index=new_index, name=series.name)
