    def _combine_match_index(self, other, func, level=None, fill_value=None,
                             try_cast=True):
        new_data = {}

        if fill_value is not None:
            raise NotImplementedError("'fill_value' argument is not supported")
        if level is not None:
            raise NotImplementedError("'level' argument is not supported")

        new_index = self.index.union(other.index)
        this = self
        if self.index is not new_index:
            this = self.reindex(new_index)

        if other.index is not new_index:
            other = other.reindex(new_index)

        for col, series in compat.iteritems(this):
            new_data[col] = func(series.values, other.values)

        # fill_value is a function of our operator
        if isna(other.fill_value) or isna(self.default_fill_value):
            fill_value = np.nan
        else:
            fill_value = func(np.float64(self.default_fill_value),
                              np.float64(other.fill_value))

        return self._constructor(
            new_data, index=new_index, columns=self.columns,
            default_fill_value=fill_value).__finalize__(self)
