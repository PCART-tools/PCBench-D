    def __iter__(self) -> Iterator[Any]:
        return self.get_columns().__iter__()
