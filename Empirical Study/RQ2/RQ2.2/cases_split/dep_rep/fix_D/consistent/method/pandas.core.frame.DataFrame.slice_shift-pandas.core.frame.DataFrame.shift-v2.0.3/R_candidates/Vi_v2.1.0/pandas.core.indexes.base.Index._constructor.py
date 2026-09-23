    @cache_readonly
    def _constructor(self) -> type[Self]:
        return type(self)
