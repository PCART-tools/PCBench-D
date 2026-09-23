    def __bool__(self) -> NoReturn:
        msg = (
            "the truth value of a Series is ambiguous"
            "\n\nHint: use '&' or '|' to chain Series boolean results together, not and/or."
            " To check if a Series contains any values, use `is_empty()`."
        )
        raise TypeError(msg)
