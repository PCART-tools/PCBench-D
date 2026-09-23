    def test_scalar_empty_dataset(self):
        """Test the scalar's cov factor for an empty array."""
        with pytest.raises(ValueError):
            mlab.GaussianKDE([], bw_method=5)
