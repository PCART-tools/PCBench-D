    @cache_readonly
    def _isnan(self) -> np.ndarray:
        # error: Incompatible return value type (got "ExtensionArray", expected
        # "ndarray")
        return self._data.isna()  # type: ignore[return-value]
