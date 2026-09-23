    def conditional_space(self, condition, normalize=True, **kwargs):
        rvs = random_symbols(condition)
        condition = condition.xreplace(dict((rv, rv.symbol) for rv in self.values))
        if any([pspace(rv).is_Continuous for rv in rvs]):
            from sympy.stats.crv import (ConditionalContinuousDomain,
                ContinuousPSpace)
            space = ContinuousPSpace
            domain = ConditionalContinuousDomain(self.domain, condition)
        elif any([pspace(rv).is_Discrete for rv in rvs]):
            from sympy.stats.drv import (ConditionalDiscreteDomain,
                DiscretePSpace)
            space = DiscretePSpace
            domain = ConditionalDiscreteDomain(self.domain, condition)
        elif all([pspace(rv).is_Finite for rv in rvs]):
            from sympy.stats.frv import FinitePSpace
            return FinitePSpace.conditional_space(self, condition)
        if normalize:
            replacement  = {rv: Dummy(str(rv)) for rv in self.symbols}
            norm = domain.compute_expectation(self.pdf, **kwargs)
            pdf = self.pdf / norm.xreplace(replacement)
            # XXX: Converting symbols from set to tuple. The order matters to
            # Lambda though so we shouldn't be starting with a set here...
            density = Lambda(tuple(domain.symbols), pdf)

        return space(domain, density)
