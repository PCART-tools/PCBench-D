    def __getstate__(self) -> list[pli.Series]:
        return self.get_columns()
