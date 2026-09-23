    def __reversed__(self) -> Iterator[Series]:
        return reversed(self.get_columns())
