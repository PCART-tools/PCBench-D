    def _sample_pymc3(self, size):
        n, a, b = int(self.n), float(self.alpha), float(self.beta)
        with pymc3.Model():
            pymc3.BetaBinomial('X', alpha=a, beta=b, n=n)
            return pymc3.sample(size, chains=1, progressbar=False)[:]['X']
