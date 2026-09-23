    def __bool__(self) -> NoReturn:
        msg = (
            "the truth value of an Expr is ambiguous"
            "\n\n"
            "You probably got here by using a Python standard library function instead "
            "of the native expressions API.\n"
            "Here are some things you might want to try:\n"
            "- instead of `pl.col('a') and pl.col('b')`, use `pl.col('a') & pl.col('b')`\n"
            "- instead of `pl.col('a') in [y, z]`, use `pl.col('a').is_in([y, z])`\n"
            "- instead of `max(pl.col('a'), pl.col('b'))`, use `pl.max_horizontal(pl.col('a'), pl.col('b'))`\n"
        )
        raise TypeError(msg)
