    def sample(self):
        scipy = import_module('scipy')
        if scipy:
            from scipy.stats import invgamma
            return invgamma.rvs(float(self.a), 0, float(self.b))
        else:
            raise NotImplementedError('Sampling the inverse Gamma Distribution requires Scipy.')
