    def _maybe_mask_result(self, result, mask, other, op_name):
        """
        Parameters
        ----------
        result : array-like
        mask : array-like bool
        other : scalar or array-like
        op_name : str
        """

        # may need to fill infs
        # and mask wraparound
        if is_float_dtype(result):
            mask |= (result == np.inf) | (result == -np.inf)

        # if we have a float operand we are by-definition
        # a float result
        # or our op is a divide
        if (is_float_dtype(other) or is_float(other)) or (
            op_name in ["rtruediv", "truediv"]
        ):
            result[mask] = np.nan
            return result

        return type(self)(result, mask, copy=False)
