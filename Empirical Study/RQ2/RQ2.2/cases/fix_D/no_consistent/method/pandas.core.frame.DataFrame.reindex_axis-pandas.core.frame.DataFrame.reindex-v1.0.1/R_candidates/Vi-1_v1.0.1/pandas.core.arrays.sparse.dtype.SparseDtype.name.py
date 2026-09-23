    @property
    def name(self):
        return f"Sparse[{self.subtype.name}, {self.fill_value}]"
