    def __getstate__(self) -> list[Series]:
        return self.get_columns()
