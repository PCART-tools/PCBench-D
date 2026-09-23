    def __add__(
        self: DF, other: DataFrame | pli.Series | int | float | bool | str
    ) -> DF:
        if isinstance(other, DataFrame):
            return self._from_pydf(self._df.add_df(other._df))
        other = _prepare_other_arg(other)
        return self._from_pydf(self._df.add(other._s))
