    @cache_readonly
    def inferred_type(self) -> str:
        return {
            "i": "integer",
            "u": "integer",
            "f": "floating",
            "c": "complex",
        }[self.dtype.kind]
