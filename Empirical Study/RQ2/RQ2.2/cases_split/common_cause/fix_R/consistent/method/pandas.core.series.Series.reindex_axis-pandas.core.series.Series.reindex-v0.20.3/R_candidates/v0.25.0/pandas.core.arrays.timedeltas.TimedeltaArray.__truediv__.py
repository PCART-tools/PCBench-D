    def __truediv__(self, other):
        # timedelta / X is well-defined for timedelta-like or numeric X
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
            return self._data / other

        elif lib.is_scalar(other):
            # assume it is numeric
            result = self._data / other
            freq = None
            if self.freq is not None:
                # Tick division is not implemented, so operate on Timedelta
                freq = self.freq.delta / other
            return type(self)(result, freq=freq)

        if not hasattr(other, "dtype"):
            # e.g. list, tuple
            other = np.array(other)

        if len(other) != len(self):
            raise ValueError("Cannot divide vectors with unequal lengths")

        elif is_timedelta64_dtype(other):
            # let numpy handle it
            return self._data / other

        elif is_object_dtype(other):
            # Note: we do not do type inference on the result, so either
            #  an object array or numeric-dtyped (if numpy does inference)
            #  will be returned.  GH#23829
            result = [self[n] / other[n] for n in range(len(self))]
            result = np.array(result)
            return result

        else:
            result = self._data / other
            return type(self)(result)
