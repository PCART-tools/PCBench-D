    def test_scott_singledim_dataset(self):
        """Use a single-dimensional array as the dataset and test scott's
        output"""
        x1 = np.array([-7, -5, 1, 4, 5])
        mygauss = mlab.GaussianKDE(x1, "scott")
        y_expected = 0.72477966367769553
        assert_almost_equal(mygauss.covariance_factor(), y_expected, 7)
