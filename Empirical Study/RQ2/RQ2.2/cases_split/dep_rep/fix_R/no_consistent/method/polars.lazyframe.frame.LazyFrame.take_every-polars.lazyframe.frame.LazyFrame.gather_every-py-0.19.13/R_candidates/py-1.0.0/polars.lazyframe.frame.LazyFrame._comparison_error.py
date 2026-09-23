    def _comparison_error(self, operator: str) -> NoReturn:
        msg = f'"{operator!r}" comparison not supported for LazyFrame objects'
        raise TypeError(msg)
