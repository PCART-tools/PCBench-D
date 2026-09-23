    @cache_readonly
    def _constructor(self) -> type[Int64Index]:  # type: ignore[override]
        """return the class to use for construction"""
        return Int64Index
