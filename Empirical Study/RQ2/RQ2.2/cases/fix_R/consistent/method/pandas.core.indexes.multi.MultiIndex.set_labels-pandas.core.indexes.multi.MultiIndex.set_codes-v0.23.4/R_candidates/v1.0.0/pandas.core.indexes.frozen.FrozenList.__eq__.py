    def __eq__(self, other: Any) -> bool:
        if isinstance(other, (tuple, FrozenList)):
            other = list(other)
        return super().__eq__(other)
