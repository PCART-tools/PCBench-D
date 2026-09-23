    def __hash__(self) -> int:
        return hash((str(self), str(self.subtype), self.closed))
