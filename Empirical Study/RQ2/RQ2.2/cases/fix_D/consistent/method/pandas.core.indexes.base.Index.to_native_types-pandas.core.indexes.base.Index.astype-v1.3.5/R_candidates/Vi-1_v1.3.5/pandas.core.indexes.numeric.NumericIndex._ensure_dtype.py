    @classmethod
    def _ensure_dtype(
        cls,
        dtype: Dtype | None,
    ) -> np.dtype | None:
        """Ensure int64 dtype for Int64Index, etc. Assumed dtype is validated."""
        return cls._default_dtype
