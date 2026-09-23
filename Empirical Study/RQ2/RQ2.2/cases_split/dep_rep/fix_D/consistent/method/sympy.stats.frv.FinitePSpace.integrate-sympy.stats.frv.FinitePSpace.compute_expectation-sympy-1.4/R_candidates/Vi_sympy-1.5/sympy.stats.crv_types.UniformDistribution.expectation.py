    def expectation(self, expr, var, **kwargs):
        from sympy import Max, Min
        kwargs['evaluate'] = True
        result = SingleContinuousDistribution.expectation(self, expr, var, **kwargs)
        result = result.subs({Max(self.left, self.right): self.right,
                              Min(self.left, self.right): self.left})
        return result
