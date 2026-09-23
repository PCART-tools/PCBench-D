    @cacheit
    def compute_characteristic_function(self, expr):
        if self._is_symbolic:
            d = self.compute_density(expr)
            t = Dummy('t', real=True)
            ki = Dummy('ki')
            return Lambda(t, Sum(d(ki)*exp(I*ki*t), (ki, self.args[1].low, self.args[1].high)))
        expr = rv_subs(expr, self.values)
        return FinitePSpace(self.domain, self.distribution).compute_characteristic_function(expr)
