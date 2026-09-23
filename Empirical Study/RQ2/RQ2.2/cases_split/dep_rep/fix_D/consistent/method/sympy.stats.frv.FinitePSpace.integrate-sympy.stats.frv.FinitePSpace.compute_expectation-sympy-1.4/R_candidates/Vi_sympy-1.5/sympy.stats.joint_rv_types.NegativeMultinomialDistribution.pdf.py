    def pdf(self, *k):
        k0, p = self.k0, self.p
        term_1 = (gamma(k0 + sum(k))*(1 - sum(p))**k0)/gamma(k0)
        term_2 = Mul.fromiter([pi**ki/factorial(ki) for pi, ki in zip(p, k)])
        return term_1 * term_2
