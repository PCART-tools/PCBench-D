    @cacheit
    def compute_moment_generating_function(self, expr, **kwargs):
        if not self.domain.set.is_Interval:
            raise NotImplementedError("Moment generating function of multivariate expressions not implemented")

        d = self.compute_density(expr, **kwargs)
        x, t = symbols('x, t', real=True, cls=Dummy)
        mgf = integrate(exp(t * x) * d(x), (x, -oo, oo), **kwargs)
        return Lambda(t, mgf)
