    def _div(self, other: Any, *, floordiv: bool) -> DataFrame:
        if isinstance(other, pl.Series):
            if floordiv:
                return self.select(F.all() // lit(other))
            return self.select(F.all() / lit(other))

        elif not isinstance(other, DataFrame):
            s = _prepare_other_arg(other, length=len(self))
            other = DataFrame([s.alias(f"n{i}") for i in range(len(self.columns))])

        orig_dtypes = other.dtypes
        other = self._cast_all_from_to(other, INTEGER_DTYPES, Float64)
        df = self._from_pydf(self._df.div_df(other._df))

        df = (
            df
            if not floordiv
            else df.with_columns([s.floor() for s in df if s.dtype.is_float()])
        )
        if floordiv:
            int_casts = [
                col(column).cast(tp)
                for i, (column, tp) in enumerate(self.schema.items())
                if tp.is_integer() and orig_dtypes[i].is_integer()
            ]
            if int_casts:
                return df.with_columns(int_casts)
        return df
