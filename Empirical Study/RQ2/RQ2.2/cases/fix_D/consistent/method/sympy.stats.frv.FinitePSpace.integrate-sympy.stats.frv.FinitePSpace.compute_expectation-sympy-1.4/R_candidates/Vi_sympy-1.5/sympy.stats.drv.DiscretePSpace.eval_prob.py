    def eval_prob(self, _domain):
        sym = list(self.symbols)[0]
        if isinstance(_domain, Range):
            n = symbols('n', integer=True)
            inf, sup, step = (r for r in _domain.args)
            summand = ((self.pdf).replace(
              sym, n*step))
            rv = summation(summand,
                (n, inf/step, (sup)/step - 1)).doit()
            return rv
        elif isinstance(_domain, FiniteSet):
            pdf = Lambda(sym, self.pdf)
            rv = sum(pdf(x) for x in _domain)
            return rv
        elif isinstance(_domain, Union):
            rv = sum(self.eval_prob(x) for x in _domain.args)
            return rv
