    def compute_density(self, expr, **kwargs):
        rvs = random_symbols(expr)
        if any(pspace(rv).is_Continuous for rv in rvs):
            z = Dummy('z', real=True)
            expr = self.compute_expectation(DiracDelta(expr - z),
             **kwargs)
        else:
            z = Dummy('z', integer=True)
            expr = self.compute_expectation(KroneckerDelta(expr, z),
             **kwargs)
        return Lambda(z, expr)
