    def __getstate__(self) -> list[Any]:
        return [self.path, self.size, self.index, self.encoding, self.layout_engine]
