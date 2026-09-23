    def __init__(
        self,
        where,
        queryables: dict[str, Any] | None = None,
        encoding=None,
        scope_level: int = 0,
    ) -> None:
        where = _validate_where(where)

        self.encoding = encoding
        self.condition = None
        self.filter = None
        self.terms = None
        self._visitor = None

        # capture the environment if needed
        local_dict: _scope.DeepChainMap[Any, Any] | None = None

        if isinstance(where, PyTablesExpr):
            local_dict = where.env.scope
            _where = where.expr

        elif is_list_like(where):
            where = list(where)
            for idx, w in enumerate(where):
                if isinstance(w, PyTablesExpr):
                    local_dict = w.env.scope
                else:
                    w = _validate_where(w)
                    where[idx] = w
            _where = " & ".join([f"({w})" for w in com.flatten(where)])
        else:
            # _validate_where ensures we otherwise have a string
            _where = where

        self.expr = _where
        self.env = PyTablesScope(scope_level + 1, local_dict=local_dict)

        if queryables is not None and isinstance(self.expr, str):
            self.env.queryables.update(queryables)
            self._visitor = PyTablesExprVisitor(
                self.env,
                queryables=queryables,
                parser="pytables",
                engine="pytables",
                encoding=encoding,
            )
            self.terms = self.parse()
