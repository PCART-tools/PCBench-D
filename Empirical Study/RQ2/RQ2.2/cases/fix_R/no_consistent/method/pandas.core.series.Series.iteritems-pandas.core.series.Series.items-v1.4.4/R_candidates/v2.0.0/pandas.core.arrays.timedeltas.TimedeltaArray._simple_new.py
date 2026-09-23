    @classmethod
    def _simple_new(  # type: ignore[override]
        cls, values: np.ndarray, freq: BaseOffset | None = None, dtype=TD64NS_DTYPE
    ) -> TimedeltaArray:
        # Require td64 dtype, not unit-less, matching values.dtype
        assert isinstance(dtype, np.dtype) and dtype.kind == "m"
        assert not tslibs.is_unitless(dtype)
        assert isinstance(values, np.ndarray), type(values)
        assert dtype == values.dtype

        result = super()._simple_new(values=values, dtype=dtype)
        result._freq = freq
        return result
