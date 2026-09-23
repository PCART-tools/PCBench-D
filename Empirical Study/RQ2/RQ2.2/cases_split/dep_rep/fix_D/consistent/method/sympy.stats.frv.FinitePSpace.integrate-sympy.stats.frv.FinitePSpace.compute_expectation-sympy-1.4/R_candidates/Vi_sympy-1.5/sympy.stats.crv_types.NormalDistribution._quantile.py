    def _quantile(self, p):
        mean, std = self.mean, self.std
        return mean + std*sqrt(2)*erfinv(2*p - 1)
