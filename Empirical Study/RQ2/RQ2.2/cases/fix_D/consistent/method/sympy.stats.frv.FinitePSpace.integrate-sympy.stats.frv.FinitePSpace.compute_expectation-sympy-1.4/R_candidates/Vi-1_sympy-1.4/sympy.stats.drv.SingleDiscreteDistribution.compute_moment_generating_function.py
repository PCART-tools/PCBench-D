    @cacheit
    def compute_moment_generating_function(self, **kwargs):
        x, t = symbols('x, t', real=True, finite=True, cls=Dummy)
        pdf = self.pdf(x)
        mgf = summation(exp(t*x)*pdf, (x, self.set.inf, self.set.sup))
        return Lambda(t, mgf)
