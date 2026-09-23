    def _apply_columns(self, func):
        """
        Get new SparseDataFrame applying func to each columns
        """

        new_data = {col: func(series) for col, series in self.items()}

        return self._constructor(
            data=new_data,
            index=self.index,
            columns=self.columns,
            default_fill_value=self.default_fill_value,
        ).__finalize__(self)
