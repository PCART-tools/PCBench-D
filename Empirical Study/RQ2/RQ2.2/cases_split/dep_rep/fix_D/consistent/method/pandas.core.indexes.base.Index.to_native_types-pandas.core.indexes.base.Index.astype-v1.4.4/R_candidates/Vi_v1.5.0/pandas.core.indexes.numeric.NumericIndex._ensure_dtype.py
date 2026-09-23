    @classmethod
    def _ensure_dtype(cls, dtype: Dtype | None) -> np.dtype | None:
        """
        Ensure int64 dtype for Int64Index etc. but allow int32 etc. for NumericIndex.

        Assumes dtype has already been validated.
        """
        if dtype is None:
            return cls._default_dtype

        dtype = pandas_dtype(dtype)
        assert isinstance(dtype, np.dtype)

        if cls._is_backward_compat_public_numeric_index:
            # dtype for NumericIndex
            return dtype
        else:
            # dtype for Int64Index, UInt64Index etc. Needed for backwards compat.
            return cls._default_dtype
