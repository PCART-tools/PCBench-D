    def __getstate__(self) -> list[Any]:
        return super().__getstate__() + [self.filename]
