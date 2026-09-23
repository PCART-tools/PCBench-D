    def _get_values_for_loc(self, series: Series, loc, key):
        """
        Do a positional lookup on the given Series, returning either a scalar
        or a Series.

        Assumes that `series.index is self`

        key is included for MultiIndex compat.
        """
        if is_integer(loc):
            return series._values[loc]

        return series.iloc[loc]
