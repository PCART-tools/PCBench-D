    def test_callable_covariance_dataset(self):
        """Use a multi-dimensional array as the dataset and test the callable's
        cov factor"""
        np.random.seed(8765678)
        n_basesample = 50
        multidim_data = [np.random.randn(n_basesample) for i in range(5)]

        def callable_fun(x):
            return 0.55
        kde = mlab.GaussianKDE(multidim_data, bw_method=callable_fun)
        assert kde.covariance_factor() == 0.55
