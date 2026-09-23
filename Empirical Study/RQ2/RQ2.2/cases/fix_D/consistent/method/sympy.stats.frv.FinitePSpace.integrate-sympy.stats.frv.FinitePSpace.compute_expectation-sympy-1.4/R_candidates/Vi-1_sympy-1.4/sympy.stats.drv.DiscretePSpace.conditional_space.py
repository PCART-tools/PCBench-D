    def conditional_space(self, condition):
        density = Lambda(self.symbols, self.pdf/self.probability(condition))
        condition = condition.xreplace(dict((rv, rv.symbol) for rv in self.values))
        domain = ConditionalDiscreteDomain(self.domain, condition)
        return DiscretePSpace(domain, density)
