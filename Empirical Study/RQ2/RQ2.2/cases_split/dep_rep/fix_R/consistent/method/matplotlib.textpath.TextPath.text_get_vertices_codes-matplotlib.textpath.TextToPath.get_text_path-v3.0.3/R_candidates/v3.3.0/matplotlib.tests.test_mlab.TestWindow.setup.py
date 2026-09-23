    def setup(self):
        np.random.seed(0)
        n = 1000

        self.sig_rand = np.random.standard_normal(n) + 100.
        self.sig_ones = np.ones(n)
