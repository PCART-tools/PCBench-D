    @unpack_zerodim_and_defer("__floordiv__")
    def __floordiv__(self, other):

        if is_scalar(other):
            if isinstance(other, self._recognized_scalars):
                other = Timedelta(other)
                if other is NaT:
                    # treat this specifically as timedelta-NaT
                    result = np.empty(self.shape, dtype=np.float64)
                    result.fill(np.nan)
                    return result

                # dispatch to Timedelta implementation
                result = other.__rfloordiv__(self._ndarray)
                return result

            # at this point we should only have numeric scalars; anything
            #  else will raise
            result = self._ndarray // other
            freq = None
            if self.freq is not None:
                # Note: freq gets division, not floor-division
                freq = self.freq / other
                if freq.nanos == 0 and self.freq.nanos != 0:
                    # e.g. if self.freq is Nano(1) then dividing by 2
                    #  rounds down to zero
                    freq = None
            return type(self)(result, freq=freq)

        if not hasattr(other, "dtype"):
            # list, tuple
            other = np.array(other)
        if len(other) != len(self):
            raise ValueError("Cannot divide with unequal lengths")

        elif is_timedelta64_dtype(other.dtype):
            other = type(self)(other)

            # numpy timedelta64 does not natively support floordiv, so operate
            #  on the i8 values
            result = self.asi8 // other.asi8
            mask = self._isnan | other._isnan
            if mask.any():
                result = result.astype(np.float64)
                np.putmask(result, mask, np.nan)
            return result

        elif is_object_dtype(other.dtype):
            # error: Incompatible types in assignment (expression has type
            # "List[Any]", variable has type "ndarray")
            srav = self.ravel()
            orav = other.ravel()
            res_list = [srav[n] // orav[n] for n in range(len(srav))]
            result_flat = np.asarray(res_list)
            inferred = lib.infer_dtype(result_flat, skipna=False)

            result = result_flat.reshape(self.shape)

            if inferred == "timedelta":
                result, _ = sequence_to_td64ns(result)
                return type(self)(result)
            if inferred == "datetime":
                # GH#39750 occurs when result is all-NaT, which in this
                #  case should be interpreted as td64nat. This can only
                #  occur when self is all-td64nat
                return self * np.nan
            return result

        elif is_integer_dtype(other.dtype) or is_float_dtype(other.dtype):
            result = self._ndarray // other
            return type(self)(result)

        else:
            dtype = getattr(other, "dtype", type(other).__name__)
            raise TypeError(f"Cannot divide {dtype} by {type(self).__name__}")
