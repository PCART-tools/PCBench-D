    def __init__(
        self,
        categorical: Categorical,
        buf: IO[str] | None = None,
        length: bool = True,
        na_rep: str = "NaN",
        footer: bool = True,
    ) -> None:
        self.categorical = categorical
        self.buf = buf if buf is not None else StringIO("")
        self.na_rep = na_rep
        self.length = length
        self.footer = footer
        self.quoting = QUOTE_NONNUMERIC
