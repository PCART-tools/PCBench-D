    def sample(self):
        """ A random realization from the distribution """
        icdf = self._inverse_cdf_expression()
        return icdf(random.uniform(0, 1))
