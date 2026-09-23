    @classmethod
    def _simple_new(  # type: ignore[override]
        cls,
        values: np.ndarray,
        freq: BaseOffset | None = None,
        dtype=DT64NS_DTYPE,
    ) -> DatetimeArray:
        assert isinstance(values, np.ndarray)
        assert dtype.kind == "M"
        if isinstance(dtype, np.dtype):
            assert dtype == values.dtype
            assert not is_unitless(dtype)
        else:
            # DatetimeTZDtype. If we have e.g. DatetimeTZDtype[us, UTC],
            #  then values.dtype should be M8[us].
            assert dtype._reso == get_unit_from_dtype(values.dtype)

        result = super()._simple_new(values, dtype)
        result._freq = freq
        return result
