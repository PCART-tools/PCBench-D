    @classmethod
    def _validate_dtype(cls, values, dtype):
        # used in TimeLikeOps.__init__
        _validate_dt64_dtype(values.dtype)
        dtype = _validate_dt64_dtype(dtype)
        return dtype
