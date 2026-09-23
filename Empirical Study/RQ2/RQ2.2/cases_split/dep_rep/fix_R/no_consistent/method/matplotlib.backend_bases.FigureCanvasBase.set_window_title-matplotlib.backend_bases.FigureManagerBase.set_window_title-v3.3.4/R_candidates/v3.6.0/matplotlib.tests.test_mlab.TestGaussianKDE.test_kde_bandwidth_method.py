    def test_kde_bandwidth_method(self):

        np.random.seed(8765678)
        n_basesample = 50
        xn = np.random.randn(n_basesample)

        # Default
        gkde = mlab.GaussianKDE(xn)
        # Supply a callable
        gkde2 = mlab.GaussianKDE(xn, 'scott')
        # Supply a scalar
        gkde3 = mlab.GaussianKDE(xn, bw_method=gkde.factor)

        xs = np.linspace(-7, 7, 51)
        kdepdf = gkde.evaluate(xs)
        kdepdf2 = gkde2.evaluate(xs)
        assert kdepdf.all() == kdepdf2.all()
        kdepdf3 = gkde3.evaluate(xs)
        assert kdepdf.all() == kdepdf3.all()
