    def __eq__(self, other: Any) -> bool:
        if isinstance(other, str):
            return other in [self.name, self.name.title()]

        return super().__eq__(other)
