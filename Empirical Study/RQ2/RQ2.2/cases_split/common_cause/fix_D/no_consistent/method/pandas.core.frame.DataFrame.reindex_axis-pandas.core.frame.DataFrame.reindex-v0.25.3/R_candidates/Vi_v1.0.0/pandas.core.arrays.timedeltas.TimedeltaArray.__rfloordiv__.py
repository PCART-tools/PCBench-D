    def __rfloordiv__(self, other):
        if isinstance(other, (ABCSeries, ABCDataFrame, ABCIndexClass)):
            return NotImplemented

        other = lib.item_from_zerodim(other)
        if is_scalar(other):
            if isinstance(other, (timedelta, np.timedelta64, Tick)):
                other = Timedelta(other)
                if other is NaT:
                    # treat this specifically as timedelta-NaT
                    result = np.empty(self.shape, dtype=np.float64)
                    result.fill(np.nan)
                    return result

                # dispatch to Timedelta implementation
                result = other.__floordiv__(self._data)
                return result

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
                result = result.astype(np.int64)
                result[mask] = np.nan
            return result

        elif is_object_dtype(other.dtype):
            result = [other[n] // self[n] for n in range(len(self))]
            result = np.array(result)
            return result

        else:
            dtype = getattr(other, "dtype", type(other).__name__)
            raise TypeError(f"Cannot divide {dtype} by {type(self).__name__}")
