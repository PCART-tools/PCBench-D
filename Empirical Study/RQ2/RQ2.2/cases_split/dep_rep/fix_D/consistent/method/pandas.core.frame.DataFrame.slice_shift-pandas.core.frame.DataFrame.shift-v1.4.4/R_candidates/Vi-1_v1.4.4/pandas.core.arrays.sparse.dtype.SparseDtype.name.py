    @property
    def name(self):
        return f"Sparse[{self.subtype.name}, {repr(self.fill_value)}]"
