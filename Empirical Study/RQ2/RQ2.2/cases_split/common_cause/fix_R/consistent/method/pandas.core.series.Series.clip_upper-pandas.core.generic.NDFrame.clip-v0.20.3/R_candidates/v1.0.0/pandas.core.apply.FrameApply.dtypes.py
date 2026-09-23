    @cache_readonly
    def dtypes(self) -> "Series":
        return self.obj.dtypes
