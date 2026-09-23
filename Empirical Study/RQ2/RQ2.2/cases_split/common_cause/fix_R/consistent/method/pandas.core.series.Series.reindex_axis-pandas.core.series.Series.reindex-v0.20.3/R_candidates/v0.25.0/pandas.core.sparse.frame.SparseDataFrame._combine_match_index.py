    def _combine_match_index(self, other, func, level=None):
        new_data = {}

        if level is not None:
            raise NotImplementedError("'level' argument is not supported")

        this, other = self.align(other, join="outer", axis=0, level=level, copy=False)

        for col, series in this.items():
            new_data[col] = func(series.values, other.values)

        fill_value = self._get_op_result_fill_value(other, func)

        return self._constructor(
            new_data,
            index=this.index,
            columns=self.columns,
            default_fill_value=fill_value,
        ).__finalize__(self)
