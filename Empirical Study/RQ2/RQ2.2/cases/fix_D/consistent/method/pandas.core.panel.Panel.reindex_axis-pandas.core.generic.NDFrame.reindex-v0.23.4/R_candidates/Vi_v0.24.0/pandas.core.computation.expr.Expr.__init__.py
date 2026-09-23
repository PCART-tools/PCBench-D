    def __init__(self, expr, engine='numexpr', parser='pandas', env=None,
                 truediv=True, level=0):
        self.expr = expr
        self.env = env or Scope(level=level + 1)
        self.engine = engine
        self.parser = parser
        self.env.scope['truediv'] = truediv
        self._visitor = _parsers[parser](self.env, self.engine, self.parser)
        self.terms = self.parse()
