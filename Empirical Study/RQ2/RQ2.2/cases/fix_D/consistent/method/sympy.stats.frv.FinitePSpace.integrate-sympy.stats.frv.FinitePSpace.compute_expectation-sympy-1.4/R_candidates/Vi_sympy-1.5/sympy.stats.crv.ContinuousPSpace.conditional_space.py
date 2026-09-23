    def conditional_space(self, condition, normalize=True, **kwargs):
        condition = condition.xreplace(dict((rv, rv.symbol) for rv in self.values))
        domain = ConditionalContinuousDomain(self.domain, condition)
        if normalize:
            # create a clone of the variable to
            # make sure that variables in nested integrals are different
            # from the variables outside the integral
            # this makes sure that they are evaluated separately
            # and in the correct order
            replacement  = {rv: Dummy(str(rv)) for rv in self.symbols}
            norm = domain.compute_expectation(self.pdf, **kwargs)
            pdf = self.pdf / norm.xreplace(replacement)
            # XXX: Converting set to tuple. The order matters to Lambda though
            # so we shouldn't be starting with a set here...
            density = Lambda(tuple(domain.symbols), pdf)

        return ContinuousPSpace(domain, density)
