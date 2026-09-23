    @cache_readonly
    def is_unsigned_integer(self) -> bool:
        return self.kind == "u"
