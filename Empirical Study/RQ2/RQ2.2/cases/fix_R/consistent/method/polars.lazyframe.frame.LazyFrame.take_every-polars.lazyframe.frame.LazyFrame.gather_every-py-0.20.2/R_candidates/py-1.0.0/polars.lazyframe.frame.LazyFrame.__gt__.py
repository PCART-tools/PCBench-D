    def __gt__(self, other: Any) -> NoReturn:
        self._comparison_error(">")
