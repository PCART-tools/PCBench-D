    def _maybe_mask_result(self, result, mask):
        """
        Parameters
        ----------
        result : array-like or tuple[array-like]
        mask : array-like bool
        """
        if isinstance(result, tuple):
            # i.e. divmod
            div, mod = result
            return (
                self._maybe_mask_result(div, mask),
                self._maybe_mask_result(mod, mask),
            )

        if is_float_dtype(result.dtype):
            from pandas.core.arrays import FloatingArray

            return FloatingArray(result, mask, copy=False)

        elif is_bool_dtype(result.dtype):
            from pandas.core.arrays import BooleanArray

            return BooleanArray(result, mask, copy=False)

        elif result.dtype == "timedelta64[ns]":
            # e.g. test_numeric_arr_mul_tdscalar_numexpr_path
            from pandas.core.arrays import TimedeltaArray

            if not isinstance(result, TimedeltaArray):
                result = TimedeltaArray._simple_new(result)

            result[mask] = result.dtype.type("NaT")
            return result

        elif is_integer_dtype(result.dtype):
            from pandas.core.arrays import IntegerArray

            return IntegerArray(result, mask, copy=False)

        else:
            result[mask] = np.nan
            return result
