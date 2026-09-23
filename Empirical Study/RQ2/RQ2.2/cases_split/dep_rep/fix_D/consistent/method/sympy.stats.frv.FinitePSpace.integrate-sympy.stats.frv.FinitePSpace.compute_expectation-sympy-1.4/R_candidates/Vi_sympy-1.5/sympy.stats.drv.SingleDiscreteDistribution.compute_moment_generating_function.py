    @cacheit
    def compute_moment_generating_function(self, **kwargs):
        t = Dummy('t', real=True)
        x = Dummy('x', integer=True)
        pdf = self.pdf(x)
        mgf = summation(exp(t*x)*pdf, (x, self.set.inf, self.set.sup))
        return Lambda(t, mgf)
