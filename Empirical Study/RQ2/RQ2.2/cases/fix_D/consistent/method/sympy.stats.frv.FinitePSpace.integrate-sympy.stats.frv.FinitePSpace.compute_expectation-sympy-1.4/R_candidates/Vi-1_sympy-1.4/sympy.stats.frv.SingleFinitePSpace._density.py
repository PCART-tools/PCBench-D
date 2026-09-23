    @property
    @cacheit
    def _density(self):
        return dict((FiniteSet((self.symbol, val)), prob)
                    for val, prob in self.distribution.dict.items())
