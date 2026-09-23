    def test_no_data(self):
        """Pass no data into the GaussianKDE class."""
        with pytest.raises(ValueError):
            mlab.GaussianKDE([])
