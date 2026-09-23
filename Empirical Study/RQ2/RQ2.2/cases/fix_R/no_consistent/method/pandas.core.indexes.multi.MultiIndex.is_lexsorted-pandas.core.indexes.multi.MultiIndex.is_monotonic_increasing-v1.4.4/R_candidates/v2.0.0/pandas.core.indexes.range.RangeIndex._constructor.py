    @cache_readonly
    def _constructor(self) -> type[Index]:  # type: ignore[override]
        """return the class to use for construction"""
        return Index
