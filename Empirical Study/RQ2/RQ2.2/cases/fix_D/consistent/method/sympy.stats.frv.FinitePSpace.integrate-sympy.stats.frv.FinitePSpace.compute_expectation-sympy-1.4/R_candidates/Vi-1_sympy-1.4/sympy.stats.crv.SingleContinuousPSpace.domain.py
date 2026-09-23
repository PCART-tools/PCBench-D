    @property
    def domain(self):
        return SingleContinuousDomain(sympify(self.symbol), self.set)
