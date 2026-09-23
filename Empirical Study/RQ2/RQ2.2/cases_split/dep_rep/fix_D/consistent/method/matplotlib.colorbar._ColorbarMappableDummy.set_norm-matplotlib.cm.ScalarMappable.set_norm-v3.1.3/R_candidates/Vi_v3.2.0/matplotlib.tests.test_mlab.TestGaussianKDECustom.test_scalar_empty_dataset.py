    def test_scalar_empty_dataset(self):
        """Use an empty array as the dataset and test the scalar's cov factor
        """
        with pytest.raises(ValueError):
            mlab.GaussianKDE([], bw_method=5)
