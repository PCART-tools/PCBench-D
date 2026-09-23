    @unpack_zerodim_and_defer("__rfloordiv__")
    def __rfloordiv__(self, other):

        if is_scalar(other):
            if isinstance(other, self._recognized_scalars):
                other = Timedelta(other)
                # mypy assumes that __new__ returns an instance of the class
                # github.com/python/mypy/issues/1020
                if cast("Timedelta | NaTType", other) is NaT:
                    # treat this specifically as timedelta-NaT
                    result = np.empty(self.shape, dtype=np.float64)
                    result.fill(np.nan)
                    return result

                # dispatch to Timedelta implementation
                return other.__floordiv__(self._ndarray)

            raise TypeError(
                f"Cannot divide {type(other).__name__} by {type(self).__name__}"
            )

        if not hasattr(other, "dtype"):
            # list, tuple
            other = np.array(other)

        if len(other) != len(self):
            raise ValueError("Cannot divide with unequal lengths")

        elif is_timedelta64_dtype(other.dtype):
            other = type(self)(other)
            # numpy timedelta64 does not natively support floordiv, so operate
            #  on the i8 values
            result = other.asi8 // self.asi8
            mask = self._isnan | other._isnan
            if mask.any():
                result = result.astype(np.float64)
                np.putmask(result, mask, np.nan)
            return result

        elif is_object_dtype(other.dtype):
            result_list = [other[n] // self[n] for n in range(len(self))]
            result = np.array(result_list)
            return result

        else:
            dtype = getattr(other, "dtype", type(other).__name__)
            raise TypeError(f"Cannot divide {dtype} by {type(self).__name__}")
