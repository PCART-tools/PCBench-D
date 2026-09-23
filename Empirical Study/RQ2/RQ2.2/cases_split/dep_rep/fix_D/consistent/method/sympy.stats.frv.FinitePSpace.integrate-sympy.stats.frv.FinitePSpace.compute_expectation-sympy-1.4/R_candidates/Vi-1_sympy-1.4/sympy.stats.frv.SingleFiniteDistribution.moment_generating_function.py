    @property
    def moment_generating_function(self):
        t = Dummy('t', real=True)
        return Lambda(t, sum(exp(k * t) * v for k, v in self.dict.items()))
