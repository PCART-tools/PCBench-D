    def __bool__(self) -> NoReturn:
        raise TypeError(
            "the truth value of a LazyFrame is ambiguous"
            "\n\nLazyFrames cannot be used in boolean context with and/or/not operators."
        )
