    def test_single_dataset_element(self):
        """Pass a single dataset element into the GaussianKDE class."""
        with pytest.raises(ValueError):
            mlab.GaussianKDE([42])
