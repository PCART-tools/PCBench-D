    @cache_readonly
    def _indicator_name(self) -> str | None:
        if isinstance(self.indicator, str):
            return self.indicator
        elif isinstance(self.indicator, bool):
            return "_merge" if self.indicator else None
        else:
            raise ValueError(
                "indicator option can only accept boolean or string arguments"
            )
