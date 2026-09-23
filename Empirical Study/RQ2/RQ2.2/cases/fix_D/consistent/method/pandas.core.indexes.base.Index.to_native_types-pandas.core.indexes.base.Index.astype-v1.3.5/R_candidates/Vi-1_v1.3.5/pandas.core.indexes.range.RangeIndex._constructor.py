    @cache_readonly
    def _constructor(self) -> type[Int64Index]:
        """return the class to use for construction"""
        return Int64Index
