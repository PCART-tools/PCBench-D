    def _validate_fill_value(self, value):
        # e.g. np.array([1]) we want np.array([1], dtype=np.uint64)
        #  see test_where_uin64
        super()._validate_fill_value(value)
        if hasattr(value, "dtype") and is_signed_integer_dtype(value.dtype):
            if (value >= 0).all():
                return value.astype(self.dtype)
            raise TypeError
        return value
