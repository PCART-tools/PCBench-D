    def pdf(self, *y):
        from sympy.functions.special.gamma_functions import gamma
        d, v, l, mu = self.delta, self.v, self.lamda, self.mu
        n = Symbol('n', negative=False, integer=True)
        k = len(l)
        sterm1 = Pow((1 - d), n)/\
                ((gamma(v + n)**(k - 1))*gamma(v)*gamma(n + 1))
        sterm2 = Mul.fromiter([mui*li**(-v - n) for mui, li in zip(mu, l)])
        term1 = sterm1 * sterm2
        sterm3 = (v + n) * sum([mui * yi for mui, yi in zip(mu, y)])
        sterm4 = sum([exp(mui * yi)/li for (mui, yi, li) in zip(mu, y, l)])
        term2 = exp(sterm3 - sterm4)
        return Pow(d, v) * Sum(term1 * term2, (n, 0, S.Infinity))
