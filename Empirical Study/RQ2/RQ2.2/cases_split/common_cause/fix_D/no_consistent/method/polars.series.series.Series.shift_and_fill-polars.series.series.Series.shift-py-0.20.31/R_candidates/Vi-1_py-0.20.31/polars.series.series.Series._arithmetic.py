    def _arithmetic(self, other: Any, op_s: str, op_ffi: str) -> Self:
        if isinstance(other, pl.Expr):
            # expand pl.lit, pl.datetime, pl.duration Exprs to compatible Series
            other = self.to_frame().select_seq(other).to_series()
        elif other is None:
            other = pl.Series("", [None])

        if isinstance(other, Series):
            return self._from_pyseries(getattr(self._s, op_s)(other._s))
        elif _check_for_numpy(other) and isinstance(other, np.ndarray):
            return self._from_pyseries(getattr(self._s, op_s)(Series(other)._s))
        elif (
            isinstance(other, (float, date, datetime, timedelta, str))
            and not self.dtype.is_float()
        ):
            _s = sequence_to_pyseries(self.name, [other])
            if "rhs" in op_ffi:
                return self._from_pyseries(getattr(_s, op_s)(self._s))
            else:
                return self._from_pyseries(getattr(self._s, op_s)(_s))

        if isinstance(other, (PyDecimal, int)) and self.dtype.is_decimal():
            _s = sequence_to_pyseries(self.name, [other], dtype=Decimal)

            if "rhs" in op_ffi:
                return self._from_pyseries(getattr(_s, op_s)(self._s))
            else:
                return self._from_pyseries(getattr(self._s, op_s)(_s))
        else:
            other = maybe_cast(other, self.dtype)
            f = get_ffi_func(op_ffi, self.dtype, self._s)
        if f is None:
            msg = (
                f"cannot do arithmetic with Series of dtype: {self.dtype!r} and argument"
                f" of type: {type(other).__name__!r}"
            )
            raise TypeError(msg)
        return self._from_pyseries(f(other))
