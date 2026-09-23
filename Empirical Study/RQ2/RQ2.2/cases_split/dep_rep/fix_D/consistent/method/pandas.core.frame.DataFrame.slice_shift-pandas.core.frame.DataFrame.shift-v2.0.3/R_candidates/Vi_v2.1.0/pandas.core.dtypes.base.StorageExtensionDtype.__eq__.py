    def __eq__(self, other: Any) -> bool:
        if isinstance(other, str) and other == self.name:
            return True
        return super().__eq__(other)
