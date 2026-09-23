    def _comp(self, other: Any, op: ComparisonOperator) -> Series:
        # special edge-case; boolean broadcast series (eq/neq) is its own result
        if self.dtype == Boolean and isinstance(other, bool) and op in ("eq", "neq"):
            if (other is True and op == "eq") or (other is False and op == "neq"):
                return self.clone()
            elif (other is False and op == "eq") or (other is True and op == "neq"):
                return ~self

        elif isinstance(other, float) and self.dtype.is_integer():
            # require upcast when comparing int series to float value
            self = self.cast(Float64)
            f = get_ffi_func(op + "_<>", Float64, self._s)
            assert f is not None
            return self._from_pyseries(f(other))

        elif isinstance(other, datetime):
            if self.dtype == Date:
                # require upcast when comparing date series to datetime
                self = self.cast(Datetime("us"))
                time_unit = "us"
            elif self.dtype == Datetime:
                # Use local time zone info
                time_zone = self.dtype.time_zone  # type: ignore[attr-defined]
                if str(other.tzinfo) != str(time_zone):
                    msg = f"Datetime time zone {other.tzinfo!r} does not match Series timezone {time_zone!r}"
                    raise TypeError(msg)
                time_unit = self.dtype.time_unit  # type: ignore[attr-defined]
            else:
                msg = f"cannot compare datetime.datetime to Series of type {self.dtype}"
                raise ValueError(msg)
            ts = _datetime_to_pl_timestamp(other, time_unit)  # type: ignore[arg-type]
            f = get_ffi_func(op + "_<>", Int64, self._s)
            assert f is not None
            return self._from_pyseries(f(ts))

        elif isinstance(other, time) and self.dtype == Time:
            d = _time_to_pl_time(other)
            f = get_ffi_func(op + "_<>", Int64, self._s)
            assert f is not None
            return self._from_pyseries(f(d))

        elif isinstance(other, timedelta) and self.dtype == Duration:
            time_unit = self.dtype.time_unit  # type: ignore[attr-defined]
            td = _timedelta_to_pl_timedelta(other, time_unit)  # type: ignore[arg-type]
            f = get_ffi_func(op + "_<>", Int64, self._s)
            assert f is not None
            return self._from_pyseries(f(td))

        elif self.dtype in [Categorical, Enum] and not isinstance(other, Series):
            other = Series([other])

        elif isinstance(other, date) and self.dtype == Date:
            d = _date_to_pl_date(other)
            f = get_ffi_func(op + "_<>", Int32, self._s)
            assert f is not None
            return self._from_pyseries(f(d))

        if isinstance(other, Sequence) and not isinstance(other, str):
            if self.dtype in (List, Array):
                other = [other]
            other = Series("", other, dtype_if_empty=self.dtype)

        if isinstance(other, Series):
            return self._from_pyseries(getattr(self._s, op)(other._s))

        if other is not None:
            other = maybe_cast(other, self.dtype)
        f = get_ffi_func(op + "_<>", self.dtype, self._s)
        if f is None:
            return NotImplemented

        return self._from_pyseries(f(other))
