    def __iter__(self) -> Iterator[Series]:
        return self.iter_columns()
