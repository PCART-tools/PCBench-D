    @cacheit
    def compute_characteristic_function(self, expr, **kwargs):
        if not self.domain.set.is_Interval:
            raise NotImplementedError("Characteristic function of multivariate expressions not implemented")

        d = self.compute_density(expr, **kwargs)
        x, t = symbols('x, t', real=True, cls=Dummy)
        cf = integrate(exp(I*t*x)*d(x), (x, -oo, oo), **kwargs)
        return Lambda(t, cf)
