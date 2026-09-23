    def __bool__(self) -> NoReturn:
        msg = (
            "the truth value of a LazyFrame is ambiguous"
            "\n\nLazyFrames cannot be used in boolean context with and/or/not operators."
        )
        raise TypeError(msg)
