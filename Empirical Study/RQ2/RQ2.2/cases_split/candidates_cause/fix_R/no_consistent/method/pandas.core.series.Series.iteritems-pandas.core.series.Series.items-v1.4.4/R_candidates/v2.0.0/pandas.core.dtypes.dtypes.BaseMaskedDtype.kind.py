    @cache_readonly
    def kind(self) -> str:
        return self.numpy_dtype.kind
