    def compute_quantile(self, expr):
        if self._is_symbolic:
            raise NotImplementedError("Computing quantile for random variables "
            "with symbolic dimension because the bounds of searching the required "
            "value is undetermined.")
        expr = rv_subs(expr, self.values)
        return FinitePSpace(self.domain, self.distribution).compute_quantile(expr)
