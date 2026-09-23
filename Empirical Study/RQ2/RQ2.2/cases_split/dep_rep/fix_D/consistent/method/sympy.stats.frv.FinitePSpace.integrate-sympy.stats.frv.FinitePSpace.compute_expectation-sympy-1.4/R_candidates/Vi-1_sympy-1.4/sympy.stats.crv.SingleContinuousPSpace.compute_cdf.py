    def compute_cdf(self, expr, **kwargs):
        if expr == self.value:
            z = symbols("z", real=True, finite=True, cls=Dummy)
            return Lambda(z, self.distribution.cdf(z, **kwargs))
        else:
            return ContinuousPSpace.compute_cdf(self, expr, **kwargs)
