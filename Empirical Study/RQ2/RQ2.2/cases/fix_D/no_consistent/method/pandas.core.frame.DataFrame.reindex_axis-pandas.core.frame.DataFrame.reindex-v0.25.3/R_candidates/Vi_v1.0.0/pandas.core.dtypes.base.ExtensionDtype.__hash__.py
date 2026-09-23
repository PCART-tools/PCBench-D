    def __hash__(self) -> int:
        return hash(tuple(getattr(self, attr) for attr in self._metadata))
