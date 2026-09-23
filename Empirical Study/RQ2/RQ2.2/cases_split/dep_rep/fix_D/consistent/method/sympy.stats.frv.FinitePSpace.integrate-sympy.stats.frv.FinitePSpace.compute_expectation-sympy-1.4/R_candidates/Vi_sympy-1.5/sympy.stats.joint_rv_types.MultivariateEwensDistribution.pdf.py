    def pdf(self, *syms):
        n, theta = self.n, self.theta
        condi = isinstance(self.n, Integer)
        if not (isinstance(syms[0], IndexedBase) or condi):
            raise ValueError("Please use IndexedBase object for syms as "
                                "the dimension is symbolic")
        term_1 = factorial(n)/rf(theta, n)
        if condi:
            term_2 = Mul.fromiter([theta**syms[j]/((j+1)**syms[j]*factorial(syms[j]))
                                    for j in range(n)])
            cond = Eq(sum([(k + 1)*syms[k] for k in range(n)]), n)
            return Piecewise((term_1 * term_2, cond), (0, True))
        syms = syms[0]
        j, k = symbols('j, k', positive=True, integer=True)
        term_2 = Product(theta**syms[j]/((j+1)**syms[j]*factorial(syms[j])),
                            (j, 0, n - 1))
        cond = Eq(Sum((k + 1)*syms[k], (k, 0, n - 1)), n)
        return Piecewise((term_1 * term_2, cond), (0, True))
