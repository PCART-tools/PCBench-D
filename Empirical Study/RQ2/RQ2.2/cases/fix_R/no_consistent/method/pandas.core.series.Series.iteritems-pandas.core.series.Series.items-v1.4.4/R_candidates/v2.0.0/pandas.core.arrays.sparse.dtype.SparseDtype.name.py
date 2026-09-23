    @property
    def name(self) -> str:
        return f"Sparse[{self.subtype.name}, {repr(self.fill_value)}]"
