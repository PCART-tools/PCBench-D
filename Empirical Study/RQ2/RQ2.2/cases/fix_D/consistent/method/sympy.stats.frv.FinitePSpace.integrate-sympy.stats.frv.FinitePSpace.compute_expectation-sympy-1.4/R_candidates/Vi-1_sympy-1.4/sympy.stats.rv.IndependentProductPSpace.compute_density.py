    def compute_density(self, expr, **kwargs):
        z = Dummy('z', real=True, finite=True)
        rvs = random_symbols(expr)
        if any(pspace(rv).is_Continuous for rv in rvs):
            expr = self.compute_expectation(DiracDelta(expr - z),
             **kwargs)
        else:
            expr = self.compute_expectation(KroneckerDelta(expr, z),
             **kwargs)
        return Lambda(z, expr)
