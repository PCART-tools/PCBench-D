    def quantile(self, x, **kwargs):
        """ Cumulative density function """
        if len(kwargs) == 0:
            quantile = self._quantile(x)
            if quantile is not None:
                return quantile
        return self.compute_quantile(**kwargs)(x)
