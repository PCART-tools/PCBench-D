    def __le__(self, other: Any) -> NoReturn:
        self._comparison_error("<=")
