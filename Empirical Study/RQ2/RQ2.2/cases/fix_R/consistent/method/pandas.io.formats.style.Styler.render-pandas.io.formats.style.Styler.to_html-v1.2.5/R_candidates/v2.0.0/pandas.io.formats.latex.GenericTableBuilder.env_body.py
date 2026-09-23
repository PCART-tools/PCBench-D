    @property
    def env_body(self) -> str:
        iterator = self._create_row_iterator(over="body")
        return "\n".join(list(iterator))
