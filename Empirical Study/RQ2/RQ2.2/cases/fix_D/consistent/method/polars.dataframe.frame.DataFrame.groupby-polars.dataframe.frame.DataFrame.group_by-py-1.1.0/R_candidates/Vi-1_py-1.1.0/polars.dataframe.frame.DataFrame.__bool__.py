    def __bool__(self) -> NoReturn:
        msg = (
            "the truth value of a DataFrame is ambiguous"
            "\n\nHint: to check if a DataFrame contains any values, use `is_empty()`."
        )
        raise TypeError(msg)
