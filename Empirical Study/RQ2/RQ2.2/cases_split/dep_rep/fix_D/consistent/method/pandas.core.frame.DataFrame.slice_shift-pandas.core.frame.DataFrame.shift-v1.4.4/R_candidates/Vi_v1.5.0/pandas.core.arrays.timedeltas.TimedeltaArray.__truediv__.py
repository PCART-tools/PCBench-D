    @unpack_zerodim_and_defer("__truediv__")
    def __truediv__(self, other):
        # timedelta / X is well-defined for timedelta-like or numeric X

        if isinstance(other, self._recognized_scalars):
            other = Timedelta(other)
            # mypy assumes that __new__ returns an instance of the class
            # github.com/python/mypy/issues/1020
            if cast("Timedelta | NaTType", other) is NaT:
                # specifically timedelta64-NaT
                result = np.empty(self.shape, dtype=np.float64)
                result.fill(np.nan)
                return result

            # otherwise, dispatch to Timedelta implementation
            return self._ndarray / other

        elif lib.is_scalar(other):
            # assume it is numeric
            result = self._ndarray / other
            freq = None
            if self.freq is not None:
                # Tick division is not implemented, so operate on Timedelta
                freq = self.freq.delta / other
                freq = to_offset(freq)
            return type(self)._simple_new(result, dtype=result.dtype, freq=freq)

        if not hasattr(other, "dtype"):
            # e.g. list, tuple
            other = np.array(other)

        if len(other) != len(self):
            raise ValueError("Cannot divide vectors with unequal lengths")

        elif is_timedelta64_dtype(other.dtype):
            # let numpy handle it
            return self._ndarray / other

        elif is_object_dtype(other.dtype):
            # We operate on raveled arrays to avoid problems in inference
            #  on NaT
            # TODO: tests with non-nano
            srav = self.ravel()
            orav = other.ravel()
            result_list = [srav[n] / orav[n] for n in range(len(srav))]
            result = np.array(result_list).reshape(self.shape)

            # We need to do dtype inference in order to keep DataFrame ops
            #  behavior consistent with Series behavior
            inferred = lib.infer_dtype(result, skipna=False)
            if inferred == "timedelta":
                flat = result.ravel()
                result = type(self)._from_sequence(flat).reshape(result.shape)
            elif inferred == "floating":
                result = result.astype(float)
            elif inferred == "datetime":
                # GH#39750 this occurs when result is all-NaT, in which case
                #  we want to interpret these NaTs as td64.
                #  We construct an all-td64NaT result.
                # error: Incompatible types in assignment (expression has type
                # "TimedeltaArray", variable has type "ndarray[Any,
                # dtype[floating[_64Bit]]]")
                result = self * np.nan  # type: ignore[assignment]

            return result

        else:
            result = self._ndarray / other
            return type(self)._simple_new(result, dtype=result.dtype)
