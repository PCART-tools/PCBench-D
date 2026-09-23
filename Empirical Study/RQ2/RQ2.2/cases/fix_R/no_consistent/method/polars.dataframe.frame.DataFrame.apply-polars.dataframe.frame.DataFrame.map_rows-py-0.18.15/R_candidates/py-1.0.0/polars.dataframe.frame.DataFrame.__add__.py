    def __add__(
        self, other: DataFrame | Series | int | float | bool | str
    ) -> DataFrame:
        if isinstance(other, DataFrame):
            return self._from_pydf(self._df.add_df(other._df))
        other = _prepare_other_arg(other)
        return self._from_pydf(self._df.add(other._s))
