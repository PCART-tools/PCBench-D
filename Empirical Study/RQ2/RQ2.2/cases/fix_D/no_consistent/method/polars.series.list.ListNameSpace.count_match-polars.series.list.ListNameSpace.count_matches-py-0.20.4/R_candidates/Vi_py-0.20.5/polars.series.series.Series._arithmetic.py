    def _arithmetic(self, other: Any, op_s: str, op_ffi: str) -> Self:
        if isinstance(other, pl.Expr):
            # expand pl.lit, pl.datetime, pl.duration Exprs to compatible Series
            other = self.to_frame().select_seq(other).to_series()
        if isinstance(other, Series):
            return self._from_pyseries(getattr(self._s, op_s)(other._s))
        if _check_for_numpy(other) and isinstance(other, np.ndarray):
            return self._from_pyseries(getattr(self._s, op_s)(Series(other)._s))
        if (
            isinstance(other, (float, date, datetime, timedelta, str))
            and not self.dtype.is_float()
        ):
            _s = sequence_to_pyseries(self.name, [other])
            if "rhs" in op_ffi:
                return self._from_pyseries(getattr(_s, op_s)(self._s))
            else:
                return self._from_pyseries(getattr(self._s, op_s)(_s))
        if isinstance(other, (PyDecimal, int)) and self.dtype.is_decimal():
            # Infer the number's scale.  Then use the max of the inferred scale and the
            # Series' scale.  At present, this will cause arithmetic to fail with a
            # PyDecimal that has a scale greater than the Series' scale, but will ensure
            # that scale is not lost.
            _s = sequence_to_pyseries(self.name, [other], dtype=Decimal)
            _s = _s.cast(
                Decimal(
                    scale=max(
                        cast(Decimal, _s.dtype()).scale, cast(Decimal, self.dtype).scale
                    )
                ),
                strict=True,
            )

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
