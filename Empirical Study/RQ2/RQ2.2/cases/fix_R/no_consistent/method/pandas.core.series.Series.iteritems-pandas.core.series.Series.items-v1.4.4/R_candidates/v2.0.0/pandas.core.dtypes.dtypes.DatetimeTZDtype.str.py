    @cache_readonly
    def str(self) -> str:  # type: ignore[override]
        return f"|M8[{self.unit}]"
