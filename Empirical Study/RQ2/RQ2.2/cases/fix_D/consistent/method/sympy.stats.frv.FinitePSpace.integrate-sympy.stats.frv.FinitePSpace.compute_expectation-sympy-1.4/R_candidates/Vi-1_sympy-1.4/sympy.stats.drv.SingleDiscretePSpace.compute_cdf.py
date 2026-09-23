    def compute_cdf(self, expr, **kwargs):
        if expr == self.value:
            x = symbols("x", real=True, cls=Dummy)
            return Lambda(x, self.distribution.cdf(x, **kwargs))
        else:
            raise NotImplementedError()
