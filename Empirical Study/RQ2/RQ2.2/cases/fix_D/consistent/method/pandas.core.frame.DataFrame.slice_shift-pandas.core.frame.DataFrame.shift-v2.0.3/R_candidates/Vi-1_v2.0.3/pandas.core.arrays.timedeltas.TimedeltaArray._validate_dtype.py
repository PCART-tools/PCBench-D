    @classmethod
    def _validate_dtype(cls, values, dtype):
        # used in TimeLikeOps.__init__
        _validate_td64_dtype(values.dtype)
        dtype = _validate_td64_dtype(dtype)
        return dtype
