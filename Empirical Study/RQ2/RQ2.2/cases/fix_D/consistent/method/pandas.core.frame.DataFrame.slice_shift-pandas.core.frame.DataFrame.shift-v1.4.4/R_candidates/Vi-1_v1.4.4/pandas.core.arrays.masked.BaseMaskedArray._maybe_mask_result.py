    def _maybe_mask_result(self, result, mask, other, op_name: str):
        """
        Parameters
        ----------
        result : array-like
        mask : array-like bool
        other : scalar or array-like
        op_name : str
        """
        # if we have a float operand we are by-definition
        # a float result
        # or our op is a divide
        if (
            (is_float_dtype(other) or is_float(other))
            or (op_name in ["rtruediv", "truediv"])
            or (is_float_dtype(self.dtype) and is_numeric_dtype(result.dtype))
        ):
            from pandas.core.arrays import FloatingArray

            return FloatingArray(result, mask, copy=False)

        elif is_bool_dtype(result):
            from pandas.core.arrays import BooleanArray

            return BooleanArray(result, mask, copy=False)

        elif result.dtype == "timedelta64[ns]":
            # e.g. test_numeric_arr_mul_tdscalar_numexpr_path
            from pandas.core.arrays import TimedeltaArray

            result[mask] = iNaT
            return TimedeltaArray._simple_new(result)

        elif is_integer_dtype(result):
            from pandas.core.arrays import IntegerArray

            return IntegerArray(result, mask, copy=False)

        else:
            result[mask] = np.nan
            return result
