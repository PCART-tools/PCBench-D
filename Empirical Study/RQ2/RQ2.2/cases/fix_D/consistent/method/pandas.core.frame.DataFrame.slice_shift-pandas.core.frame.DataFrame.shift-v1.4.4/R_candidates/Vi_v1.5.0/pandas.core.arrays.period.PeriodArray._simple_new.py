    @classmethod
    def _simple_new(  # type: ignore[override]
        cls,
        values: np.ndarray,
        freq: BaseOffset | None = None,
        dtype: Dtype | None = None,
    ) -> PeriodArray:
        # alias for PeriodArray.__init__
        assertion_msg = "Should be numpy array of type i8"
        assert isinstance(values, np.ndarray) and values.dtype == "i8", assertion_msg
        return cls(values, freq=freq, dtype=dtype)
