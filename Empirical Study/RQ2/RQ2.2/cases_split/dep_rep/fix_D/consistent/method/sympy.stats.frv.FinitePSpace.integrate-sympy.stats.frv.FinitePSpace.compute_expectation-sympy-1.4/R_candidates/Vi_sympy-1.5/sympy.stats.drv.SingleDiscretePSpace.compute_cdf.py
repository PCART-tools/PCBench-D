    def compute_cdf(self, expr, **kwargs):
        if expr == self.value:
            x = Dummy("x", real=True)
            return Lambda(x, self.distribution.cdf(x, **kwargs))
        else:
            raise NotImplementedError()
