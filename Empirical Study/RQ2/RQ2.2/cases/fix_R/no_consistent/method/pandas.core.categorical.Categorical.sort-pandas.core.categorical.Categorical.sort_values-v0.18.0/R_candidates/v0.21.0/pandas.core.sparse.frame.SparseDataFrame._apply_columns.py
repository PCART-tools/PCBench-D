    def _apply_columns(self, func):
        """ get new SparseDataFrame applying func to each columns """

        new_data = {}
        for col, series in compat.iteritems(self):
            new_data[col] = func(series)

        return self._constructor(
            data=new_data, index=self.index, columns=self.columns,
            default_fill_value=self.default_fill_value).__finalize__(self)
