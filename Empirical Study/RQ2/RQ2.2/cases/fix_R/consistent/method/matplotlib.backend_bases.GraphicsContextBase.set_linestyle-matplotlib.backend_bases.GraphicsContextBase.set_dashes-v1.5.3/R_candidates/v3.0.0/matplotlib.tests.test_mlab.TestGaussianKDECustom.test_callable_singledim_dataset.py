    def test_callable_singledim_dataset(self):
        """Use a single-dimensional array as the dataset and test the
        callable's cov factor"""
        np.random.seed(8765678)
        n_basesample = 50
        multidim_data = np.random.randn(n_basesample)

        kde = mlab.GaussianKDE(multidim_data, bw_method='silverman')
        y_expected = 0.48438841363348911
        assert_almost_equal(kde.covariance_factor(), y_expected, 7)
