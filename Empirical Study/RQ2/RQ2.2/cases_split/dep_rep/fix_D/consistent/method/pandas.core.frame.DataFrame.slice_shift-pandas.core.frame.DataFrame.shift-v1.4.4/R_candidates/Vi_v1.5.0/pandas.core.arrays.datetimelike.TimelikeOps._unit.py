    @cache_readonly
    def _unit(self) -> str:
        # e.g. "ns", "us", "ms"
        # error: Argument 1 to "dtype_to_unit" has incompatible type
        # "ExtensionDtype"; expected "Union[DatetimeTZDtype, dtype[Any]]"
        return dtype_to_unit(self.dtype)  # type: ignore[arg-type]
