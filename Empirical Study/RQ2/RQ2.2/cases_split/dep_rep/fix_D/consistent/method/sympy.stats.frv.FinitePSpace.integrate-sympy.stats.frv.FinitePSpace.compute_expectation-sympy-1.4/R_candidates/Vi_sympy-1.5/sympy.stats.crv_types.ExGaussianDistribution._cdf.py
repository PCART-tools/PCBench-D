    def _cdf(self, x):
        from sympy.stats import cdf
        mean, std, rate = self.mean, self.std, self.rate
        u = rate*(x - mean)
        v = rate*std
        GaussianCDF1 = cdf(Normal('x', 0, v))(u)
        GaussianCDF2 = cdf(Normal('x', v**2, v))(u)

        return GaussianCDF1 - exp(-u + (v**2/2) + log(GaussianCDF2))
