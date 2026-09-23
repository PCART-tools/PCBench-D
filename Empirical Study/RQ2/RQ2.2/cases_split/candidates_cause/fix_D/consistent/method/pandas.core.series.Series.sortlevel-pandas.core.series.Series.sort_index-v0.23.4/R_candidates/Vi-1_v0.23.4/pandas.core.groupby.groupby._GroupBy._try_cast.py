    def _try_cast(self, result, obj, numeric_only=False):
        """
        try to cast the result to our obj original type,
        we may have roundtripped thru object in the mean-time

        if numeric_only is True, then only try to cast numerics
        and not datetimelikes

        """
        if obj.ndim > 1:
            dtype = obj.values.dtype
        else:
            dtype = obj.dtype

        if not is_scalar(result):
            if numeric_only and is_numeric_dtype(dtype) or not numeric_only:
                result = maybe_downcast_to_dtype(result, dtype)

        return result
