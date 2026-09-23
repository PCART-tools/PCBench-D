    def _div(self: DF, other: Any, floordiv: bool) -> DF:
        if isinstance(other, pli.Series):
            other = other.to_frame()
        elif not isinstance(other, DataFrame):
            s = _prepare_other_arg(other, length=len(self))
            other = DataFrame([s.rename(f"n{i}") for i in range(len(self.columns))])

        orig_dtypes = other.dtypes
        other = self._cast_all_from_to(other, INTEGER_DTYPES, Float64)
        df = self._from_pydf(self._df.div_df(other._df))
        df = (
            df  # type: ignore[assignment]
            if not floordiv
            else df.with_columns([s.floor() for s in df if s.dtype() in FLOAT_DTYPES])
        )
        if floordiv:
            int_casts = [
                pli.col(col).cast(tp)
                for i, (col, tp) in enumerate(self.schema.items())
                if tp in INTEGER_DTYPES and orig_dtypes[i] in INTEGER_DTYPES
            ]
            if int_casts:
                return df.with_columns(int_casts)  # type: ignore[return-value]
        return df
