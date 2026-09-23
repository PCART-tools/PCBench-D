    def sample(self):
        scipy = import_module('scipy')
        if scipy:
            from scipy.stats import invgauss
            return invgauss.rvs(float(self.mean/self.shape), 0, float(self.shape))
        else:
            raise NotImplementedError(
                'Sampling the Inverse Gaussian Distribution requires Scipy.')
