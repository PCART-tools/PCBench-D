    @property
    def characteristic_function(self):
        t = Dummy('t', real=True)
        return Lambda(t, sum(exp(I*k*t)*v for k, v in self.dict.items()))
