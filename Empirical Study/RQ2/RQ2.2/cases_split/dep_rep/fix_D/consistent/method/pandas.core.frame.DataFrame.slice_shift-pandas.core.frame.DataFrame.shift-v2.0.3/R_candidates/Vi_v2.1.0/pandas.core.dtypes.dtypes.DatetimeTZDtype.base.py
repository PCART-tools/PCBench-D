    @cache_readonly
    def base(self) -> DtypeObj:  # type: ignore[override]
        return np.dtype(f"M8[{self.unit}]")
