    def compute_quantile(self, expr, **kwargs):
        if expr == self.value:
            p = Dummy("p", real=True)
            return Lambda(p, self.distribution.quantile(p, **kwargs))
        else:
            raise NotImplementedError()
