    def conditional_space(self, condition):
        # XXX: Converting from set to tuple. The order matters to Lambda
        # though so we should be starting with a set...
        density = Lambda(tuple(self.symbols), self.pdf/self.probability(condition))
        condition = condition.xreplace(dict((rv, rv.symbol) for rv in self.values))
        domain = ConditionalDiscreteDomain(self.domain, condition)
        return DiscretePSpace(domain, density)
