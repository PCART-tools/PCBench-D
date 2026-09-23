    @classmethod
    def _simple_new(  # type: ignore[override]
        cls, values: np.ndarray, freq: BaseOffset | None = None, dtype=DT64NS_DTYPE
    ) -> DatetimeArray:
        assert isinstance(values, np.ndarray)
        assert values.dtype == DT64NS_DTYPE

        result = super()._simple_new(values, dtype)
        result._freq = freq
        return result
