    def __hash__(self) -> int:  # type: ignore[override]
        return hash(tuple(self))
