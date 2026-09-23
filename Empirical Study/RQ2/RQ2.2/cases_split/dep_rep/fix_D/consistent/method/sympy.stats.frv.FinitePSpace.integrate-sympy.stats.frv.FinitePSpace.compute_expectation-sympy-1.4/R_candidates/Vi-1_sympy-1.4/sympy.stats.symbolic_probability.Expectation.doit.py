    def doit(self, **hints):
        expr = self.args[0]
        condition = self._condition

        if not expr.has(RandomSymbol):
            return expr

        if isinstance(expr, Add):
            return Add(*[Expectation(a, condition=condition).doit() for a in expr.args])
        elif isinstance(expr, Mul):
            rv = []
            nonrv = []
            for a in expr.args:
                if isinstance(a, RandomSymbol) or a.has(RandomSymbol):
                    rv.append(a)
                else:
                    nonrv.append(a)
            return Mul(*nonrv)*Expectation(Mul(*rv), condition=condition)

        return self
