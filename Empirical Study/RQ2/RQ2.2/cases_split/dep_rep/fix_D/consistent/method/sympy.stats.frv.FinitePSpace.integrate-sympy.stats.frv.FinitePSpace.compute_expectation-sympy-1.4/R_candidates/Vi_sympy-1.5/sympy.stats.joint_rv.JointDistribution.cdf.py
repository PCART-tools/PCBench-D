    def cdf(self, other):
        if not isinstance(other, dict):
            raise ValueError("%s should be of type dict, got %s"%(other, type(other)))
        rvs = other.keys()
        _set = self.domain.set.sets
        expr = self.pdf(tuple(i.args[0] for i in self.symbols))
        for i in range(len(other)):
            if rvs[i].is_Continuous:
                density = Integral(expr, (rvs[i], _set[i].inf,
                    other[rvs[i]]))
            elif rvs[i].is_Discrete:
                density = Sum(expr, (rvs[i], _set[i].inf,
                    other[rvs[i]]))
        return density
