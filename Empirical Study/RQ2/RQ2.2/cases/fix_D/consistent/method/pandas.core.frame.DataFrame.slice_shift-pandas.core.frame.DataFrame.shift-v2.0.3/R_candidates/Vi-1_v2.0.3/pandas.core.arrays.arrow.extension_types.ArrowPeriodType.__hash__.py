    def __hash__(self) -> int:
        return hash((str(self), self.freq))
