    @cache_readonly
    def is_signed_integer(self) -> bool:
        return self.kind == "i"
