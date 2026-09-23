    def test_scalar_covariance_dataset(self):
        """Use a dataset and test a scalar's cov factor
        """
        np.random.seed(8765678)
        n_basesample = 50
        multidim_data = [np.random.randn(n_basesample) for i in range(5)]

        kde = mlab.GaussianKDE(multidim_data, bw_method=0.5)
        assert kde.covariance_factor() == 0.5
