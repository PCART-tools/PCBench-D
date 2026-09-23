    def _try_cast(self, result, obj):
        """
        try to cast the result to our obj original type,
        we may have roundtripped thru object in the mean-time

        """
        if obj.ndim > 1:
            dtype = obj.values.dtype
        else:
            dtype = obj.dtype

        if not is_scalar(result):
            result = _possibly_downcast_to_dtype(result, dtype)

        return result
