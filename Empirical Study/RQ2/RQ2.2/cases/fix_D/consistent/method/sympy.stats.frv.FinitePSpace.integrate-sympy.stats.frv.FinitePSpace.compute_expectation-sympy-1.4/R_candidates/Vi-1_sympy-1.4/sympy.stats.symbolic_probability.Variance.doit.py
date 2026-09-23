    def doit(self, **hints):
        arg = self.args[0]
        condition = self._condition

        if not arg.has(RandomSymbol):
            return S.Zero

        if isinstance(arg, RandomSymbol):
            return self
        elif isinstance(arg, Add):
            rv = []
            for a in arg.args:
                if a.has(RandomSymbol):
                    rv.append(a)
            variances = Add(*map(lambda xv: Variance(xv, condition).doit(), rv))
            map_to_covar = lambda x: 2*Covariance(*x, condition=condition).doit()
            covariances = Add(*map(map_to_covar, itertools.combinations(rv, 2)))
            return variances + covariances
        elif isinstance(arg, Mul):
            nonrv = []
            rv = []
            for a in arg.args:
                if a.has(RandomSymbol):
                    rv.append(a)
                else:
                    nonrv.append(a**2)
            if len(rv) == 0:
                return S.Zero
            return Mul(*nonrv)*Variance(Mul(*rv), condition)

        # this expression contains a RandomSymbol somehow:
        return self
