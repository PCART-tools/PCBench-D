    def _get_values_for_loc(self, series: Series, loc, key):
        """
        Do a positional lookup on the given Series, returning either a scalar
        or a Series.

        Assumes that `series.index is self`
        """
        new_values = series._values[loc]
        if is_scalar(loc):
            return new_values

        if len(new_values) == 1 and not self.nlevels > 1:
            # If more than one level left, we can not return a scalar
            return new_values[0]

        new_index = self[loc]
        new_index = maybe_droplevels(new_index, key)
        new_ser = series._constructor(new_values, index=new_index, name=series.name)
        return new_ser.__finalize__(series)
