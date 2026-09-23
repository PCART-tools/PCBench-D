    @classmethod
    def _simple_new(  # type: ignore[override]
        cls,
        values: npt.NDArray[np.int64],
        dtype: PeriodDtype,
    ) -> Self:
        # alias for PeriodArray.__init__
        assertion_msg = "Should be numpy array of type i8"
        assert isinstance(values, np.ndarray) and values.dtype == "i8", assertion_msg
        return cls(values, dtype=dtype)
