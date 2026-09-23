    def __mod__(self: DF, other: DataFrame | pli.Series | int | float) -> DF:
        if isinstance(other, DataFrame):
            return self._from_pydf(self._df.rem_df(other._df))
        other = _prepare_other_arg(other)
        return self._from_pydf(self._df.rem(other._s))
