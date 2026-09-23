    @cacheit
    def compute_moment_generating_function(self, expr):
        d = self.compute_density(expr)
        t = Dummy('t', real=True)

        return Lambda(t, sum(exp(k * t) * v for k, v in d.items()))
