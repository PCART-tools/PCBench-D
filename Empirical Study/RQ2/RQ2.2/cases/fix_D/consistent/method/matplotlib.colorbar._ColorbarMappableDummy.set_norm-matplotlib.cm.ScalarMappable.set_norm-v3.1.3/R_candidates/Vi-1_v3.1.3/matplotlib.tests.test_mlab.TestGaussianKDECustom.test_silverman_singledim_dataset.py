    def test_silverman_singledim_dataset(self):
        """Use a single dimension list as the dataset and test silverman's
        output."""
        x1 = np.array([-7, -5, 1, 4, 5])
        mygauss = mlab.GaussianKDE(x1, "silverman")
        y_expected = 0.76770389927475502
        assert_almost_equal(mygauss.covariance_factor(), y_expected, 7)
