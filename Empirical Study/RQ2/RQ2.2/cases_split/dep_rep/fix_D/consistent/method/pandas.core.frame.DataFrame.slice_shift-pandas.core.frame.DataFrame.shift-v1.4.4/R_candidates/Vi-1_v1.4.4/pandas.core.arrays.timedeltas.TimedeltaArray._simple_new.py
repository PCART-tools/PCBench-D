    @classmethod
    def _simple_new(  # type: ignore[override]
        cls, values: np.ndarray, freq: BaseOffset | None = None, dtype=TD64NS_DTYPE
    ) -> TimedeltaArray:
        assert dtype == TD64NS_DTYPE, dtype
        assert isinstance(values, np.ndarray), type(values)
        assert values.dtype == TD64NS_DTYPE

        result = super()._simple_new(values=values, dtype=TD64NS_DTYPE)
        result._freq = freq
        return result
