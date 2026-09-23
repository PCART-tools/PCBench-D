    def __hash__(self) -> int:  # type: ignore[override]
        return self._val.__hash__()
