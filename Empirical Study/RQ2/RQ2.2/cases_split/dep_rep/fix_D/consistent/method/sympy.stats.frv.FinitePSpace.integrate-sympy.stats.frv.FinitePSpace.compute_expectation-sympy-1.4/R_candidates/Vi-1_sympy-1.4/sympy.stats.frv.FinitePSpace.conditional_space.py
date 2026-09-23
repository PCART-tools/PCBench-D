    def conditional_space(self, condition):
        domain = self.where(condition)
        prob = self.probability(condition)
        density = dict((key, val / prob)
                for key, val in self._density.items() if domain._test(key))
        return FinitePSpace(domain, density)
