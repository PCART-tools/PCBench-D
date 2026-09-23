    @cache_readonly
    def _constructor(self: _IndexT) -> type[_IndexT]:
        return type(self)
