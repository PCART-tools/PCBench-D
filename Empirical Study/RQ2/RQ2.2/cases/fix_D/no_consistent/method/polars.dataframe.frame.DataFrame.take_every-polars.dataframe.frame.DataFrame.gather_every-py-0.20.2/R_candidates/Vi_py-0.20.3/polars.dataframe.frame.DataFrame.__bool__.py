    def __bool__(self) -> NoReturn:
        raise TypeError(
            "the truth value of a DataFrame is ambiguous"
            "\n\nHint: to check if a DataFrame contains any values, use `is_empty()`."
        )
