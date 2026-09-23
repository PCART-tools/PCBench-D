    @property
    def header(self) -> str:
        iterator = self._create_row_iterator(over="header")
        return "\n".join(list(iterator))
