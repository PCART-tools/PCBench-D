    def pdf(self, *x):
        n, p = self.n, self.p
        term_1 = factorial(n)/Mul.fromiter([factorial(x_k) for x_k in x])
        term_2 = Mul.fromiter([p_k**x_k for p_k, x_k in zip(p, x)])
        return Piecewise((term_1 * term_2, Eq(sum(x), n)), (0, True))
