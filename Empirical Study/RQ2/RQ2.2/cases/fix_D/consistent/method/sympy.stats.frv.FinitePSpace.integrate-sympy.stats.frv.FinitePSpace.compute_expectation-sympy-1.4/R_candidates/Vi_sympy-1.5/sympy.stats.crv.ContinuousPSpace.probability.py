    def probability(self, condition, **kwargs):
        z = Dummy('z', real=True)
        cond_inv = False
        if isinstance(condition, Ne):
            condition = Eq(condition.args[0], condition.args[1])
            cond_inv = True
        # Univariate case can be handled by where
        try:
            domain = self.where(condition)
            rv = [rv for rv in self.values if rv.symbol == domain.symbol][0]
            # Integrate out all other random variables
            pdf = self.compute_density(rv, **kwargs)
            # return S.Zero if `domain` is empty set
            if domain.set is S.EmptySet or isinstance(domain.set, FiniteSet):
                return S.Zero if not cond_inv else S.One
            if isinstance(domain.set, Union):
                return sum(
                     Integral(pdf(z), (z, subset), **kwargs) for subset in
                     domain.set.args if isinstance(subset, Interval))
            # Integrate out the last variable over the special domain
            return Integral(pdf(z), (z, domain.set), **kwargs)

        # Other cases can be turned into univariate case
        # by computing a density handled by density computation
        except NotImplementedError:
            from sympy.stats.rv import density
            expr = condition.lhs - condition.rhs
            dens = density(expr, **kwargs)
            if not isinstance(dens, ContinuousDistribution):
                dens = ContinuousDistributionHandmade(dens)
            # Turn problem into univariate case
            space = SingleContinuousPSpace(z, dens)
            result = space.probability(condition.__class__(space.value, 0))
            return result if not cond_inv else S.One - result
