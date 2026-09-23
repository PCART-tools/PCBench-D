    def __bool__(self) -> NoReturn:
        raise TypeError(
            "the truth value of an Expr is ambiguous"
            "\n\nHint: use '&' or '|' to logically combine Expr, not 'and'/'or', and"
            " use `x.is_in([y,z])` instead of `x in [y,z]` to check membership."
        )
