    def setup(self):
        np.random.seed(0)
        n = 1000
        x = np.linspace(0., 100, n)

        self.sig_zeros = np.zeros(n)

        self.sig_off = self.sig_zeros + 100.
        self.sig_slope = np.linspace(-10., 90., n)

        self.sig_slope_mean = x - x.mean()

        sig_rand = np.random.standard_normal(n)
        sig_sin = np.sin(x*2*np.pi/(n/100))

        sig_rand -= sig_rand.mean()
        sig_sin -= sig_sin.mean()

        self.sig_base = sig_rand + sig_sin

        self.atol = 1e-08
