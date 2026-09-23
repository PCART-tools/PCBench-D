    def compute_cdf(self, expr, **kwargs):
        if expr == self.value:
            z = Dummy("z", real=True)
            return Lambda(z, self.distribution.cdf(z, **kwargs))
        else:
            return ContinuousPSpace.compute_cdf(self, expr, **kwargs)
