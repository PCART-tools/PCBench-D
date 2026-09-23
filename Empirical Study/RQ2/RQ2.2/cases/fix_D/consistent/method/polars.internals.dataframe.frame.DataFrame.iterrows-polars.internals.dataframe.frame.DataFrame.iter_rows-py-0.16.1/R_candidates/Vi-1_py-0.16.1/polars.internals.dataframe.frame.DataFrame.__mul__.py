    def __mul__(self: DF, other: DataFrame | pli.Series | int | float) -> DF:
        if isinstance(other, DataFrame):
            return self._from_pydf(self._df.mul_df(other._df))

        other = _prepare_other_arg(other)
        return self._from_pydf(self._df.mul(other._s))
