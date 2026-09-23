    def __init__(
        self,
        expr,
        engine: str = "numexpr",
        parser: str = "pandas",
        env: Optional[Scope] = None,
        level: int = 0,
    ):
        self.expr = expr
        self.env = env or Scope(level=level + 1)
        self.engine = engine
        self.parser = parser
        self._visitor = _parsers[parser](self.env, self.engine, self.parser)
        self.terms = self.parse()
