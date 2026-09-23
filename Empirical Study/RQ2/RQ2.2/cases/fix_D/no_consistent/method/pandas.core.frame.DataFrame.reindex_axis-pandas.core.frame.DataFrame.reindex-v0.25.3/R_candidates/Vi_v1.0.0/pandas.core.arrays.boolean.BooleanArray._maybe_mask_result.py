    def _maybe_mask_result(self, result, mask, other, op_name):
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
        if (is_float_dtype(other) or is_float(other)) or (
            op_name in ["rtruediv", "truediv"]
        ):
            result[mask] = np.nan
            return result

        if is_bool_dtype(result):
            return BooleanArray(result, mask, copy=False)

        elif is_integer_dtype(result):
            from pandas.core.arrays import IntegerArray

            return IntegerArray(result, mask, copy=False)
        else:
            result[mask] = np.nan
            return result
