    def __bool__(self) -> NoReturn:
        raise ValueError(
            "The truth value of a DataFrame is ambiguous. "
            "Hint: to check if a DataFrame contains any values, use 'is_empty()'"
        )
