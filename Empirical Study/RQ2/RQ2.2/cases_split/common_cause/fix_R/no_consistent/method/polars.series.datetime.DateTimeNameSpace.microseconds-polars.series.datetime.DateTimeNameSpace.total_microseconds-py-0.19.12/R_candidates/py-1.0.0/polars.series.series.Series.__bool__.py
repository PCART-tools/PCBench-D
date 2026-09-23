    def __bool__(self) -> NoReturn:
        msg = (
            "the truth value of a Series is ambiguous"
            "\n\n"
            "Here are some things you might want to try:\n"
            "- instead of `if s`, use `if not s.is_empty()`\n"
            "- instead of `s1 and s2`, use `s1 & s2`\n"
            "- instead of `s1 or s2`, use `s1 | s2`\n"
            "- instead of `s in [y, z]`, use `s.is_in([y, z])`\n"
        )
        raise TypeError(msg)
