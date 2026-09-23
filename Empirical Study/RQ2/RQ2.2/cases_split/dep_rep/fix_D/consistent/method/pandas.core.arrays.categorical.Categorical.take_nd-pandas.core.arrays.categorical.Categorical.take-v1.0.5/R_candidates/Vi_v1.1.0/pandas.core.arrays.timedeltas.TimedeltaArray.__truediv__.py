    @unpack_zerodim_and_defer("__truediv__")
    def __truediv__(self, other):
        # timedelta / X is well-defined for timedelta-like or numeric X

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

        elif is_timedelta64_dtype(other.dtype):
            # let numpy handle it
            return self._data / other

        elif is_object_dtype(other.dtype):
            # We operate on raveled arrays to avoid problems in inference
            #  on NaT
            srav = self.ravel()
            orav = other.ravel()
            result = [srav[n] / orav[n] for n in range(len(srav))]
            result = np.array(result).reshape(self.shape)

            # We need to do dtype inference in order to keep DataFrame ops
            #  behavior consistent with Series behavior
            inferred = lib.infer_dtype(result)
            if inferred == "timedelta":
                flat = result.ravel()
                result = type(self)._from_sequence(flat).reshape(result.shape)
            elif inferred == "floating":
                result = result.astype(float)

            return result

        else:
            result = self._data / other
            return type(self)(result)
