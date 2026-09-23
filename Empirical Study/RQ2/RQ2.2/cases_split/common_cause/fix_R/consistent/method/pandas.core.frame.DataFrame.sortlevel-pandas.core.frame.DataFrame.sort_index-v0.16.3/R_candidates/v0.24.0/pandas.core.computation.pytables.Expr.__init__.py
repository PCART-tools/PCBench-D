    def __init__(self, where, queryables=None, encoding=None, scope_level=0):

        where = _validate_where(where)

        self.encoding = encoding
        self.condition = None
        self.filter = None
        self.terms = None
        self._visitor = None

        # capture the environment if needed
        local_dict = DeepChainMap()

        if isinstance(where, Expr):
            local_dict = where.env.scope
            where = where.expr

        elif isinstance(where, (list, tuple)):
            for idx, w in enumerate(where):
                if isinstance(w, Expr):
                    local_dict = w.env.scope
                else:
                    w = _validate_where(w)
                    where[idx] = w
            where = ' & '.join(map('({})'.format, com.flatten(where)))  # noqa

        self.expr = where
        self.env = Scope(scope_level + 1, local_dict=local_dict)

        if queryables is not None and isinstance(self.expr, string_types):
            self.env.queryables.update(queryables)
            self._visitor = ExprVisitor(self.env, queryables=queryables,
                                        parser='pytables', engine='pytables',
                                        encoding=encoding)
            self.terms = self.parse()
