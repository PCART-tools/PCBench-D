    def _comparison_error(self, operator: str) -> NoReturn:
        raise TypeError(
            f'"{operator!r}" comparison not supported for LazyFrame objects'
        )
