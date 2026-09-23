    @cache_readonly
    def dtype(self) -> DtypeObj:
        return self.values.dtype
