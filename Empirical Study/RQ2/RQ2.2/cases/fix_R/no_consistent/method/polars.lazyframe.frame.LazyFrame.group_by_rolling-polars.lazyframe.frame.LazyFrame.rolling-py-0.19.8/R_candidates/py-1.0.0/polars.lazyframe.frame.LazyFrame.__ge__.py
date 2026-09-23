    def __ge__(self, other: Any) -> NoReturn:
        self._comparison_error(">=")
