    def compute_characteristic_function(self, expr, **kwargs):
        if expr == self.value:
            t = symbols("t", real=True, cls=Dummy)
            return Lambda(t, self.distribution.characteristic_function(t, **kwargs))
        else:
            return ContinuousPSpace.compute_characteristic_function(self, expr, **kwargs)
