    def compute_moment_generating_function(self, expr, **kwargs):
        if expr == self.value:
            t = symbols("t", real=True, cls=Dummy)
            return Lambda(t, self.distribution.moment_generating_function(t, **kwargs))
        else:
            return ContinuousPSpace.compute_moment_generating_function(self, expr, **kwargs)
