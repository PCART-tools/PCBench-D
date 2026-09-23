    @cache_readonly
    def inferred_type(self) -> str:
        return {
            "i": "integer",
            "u": "integer",
            "f": "floating",
        }[self.dtype.kind]
