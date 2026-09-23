    def __rtruediv__(self, other):
        # X / timedelta is defined only for timedelta-like X
        other = lib.item_from_zerodim(other)

        if isinstance(other, (ABCSeries, ABCDataFrame, ABCIndexClass)):
            return NotImplemented

        if isinstance(other, (timedelta, np.timedelta64, Tick)):
            other = Timedelta(other)
            if other is NaT:
                # specifically timedelta64-NaT
                result = np.empty(self.shape, dtype=np.float64)
                result.fill(np.nan)
                return result

            # otherwise, dispatch to Timedelta implementation
            return other / self._data

        elif lib.is_scalar(other):
            raise TypeError(
                f"Cannot divide {type(other).__name__} by {type(self).__name__}"
            )

        if not hasattr(other, "dtype"):
            # e.g. list, tuple
            other = np.array(other)

        if len(other) != len(self):
            raise ValueError("Cannot divide vectors with unequal lengths")

        elif is_timedelta64_dtype(other.dtype):
            # let numpy handle it
            return other / self._data

        elif is_object_dtype(other.dtype):
            # Note: unlike in __truediv__, we do not _need_ to do type
            #  inference on the result.  It does not raise, a numeric array
            #  is returned.  GH#23829
            result = [other[n] / self[n] for n in range(len(self))]
            return np.array(result)

        else:
            raise TypeError(
                f"Cannot divide {other.dtype} data by {type(self).__name__}"
            )
