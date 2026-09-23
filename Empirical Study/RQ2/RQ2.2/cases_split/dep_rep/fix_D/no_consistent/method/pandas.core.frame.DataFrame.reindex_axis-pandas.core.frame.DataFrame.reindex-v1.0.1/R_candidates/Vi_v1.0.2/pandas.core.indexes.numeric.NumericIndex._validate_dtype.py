    @classmethod
    def _validate_dtype(cls, dtype: Dtype) -> None:
        if dtype is None:
            return
        validation_metadata = {
            "int64index": (is_signed_integer_dtype, "signed integer"),
            "uint64index": (is_unsigned_integer_dtype, "unsigned integer"),
            "float64index": (is_float_dtype, "float"),
            "rangeindex": (is_signed_integer_dtype, "signed integer"),
        }

        validation_func, expected = validation_metadata[cls._typ]
        if not validation_func(dtype):
            raise ValueError(
                f"Incorrect `dtype` passed: expected {expected}, received {dtype}"
            )
