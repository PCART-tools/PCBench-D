    def __eq__(self, other: Any) -> bool:
        if isinstance(other, str) and other == "string":
            return True
        return super().__eq__(other)
