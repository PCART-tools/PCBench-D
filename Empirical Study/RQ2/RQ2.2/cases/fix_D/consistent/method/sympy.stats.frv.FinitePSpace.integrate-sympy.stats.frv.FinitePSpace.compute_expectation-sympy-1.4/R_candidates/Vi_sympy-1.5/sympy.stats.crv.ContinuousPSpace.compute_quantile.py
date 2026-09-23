    @cacheit
    def compute_quantile(self, expr, **kwargs):
        if not self.domain.set.is_Interval:
            raise ValueError(
                "Quantile not well defined on multivariate expressions")

        d = self.compute_cdf(expr, **kwargs)
        x = Dummy('x', real=True)
        p = Dummy('p', positive=True)

        quantile = solveset(d(x) - p, x, self.set)

        return Lambda(p, quantile)
