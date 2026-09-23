    def test_silverman_multidim_dataset(self):
        """Use a multi-dimensional array as the dataset and test silverman's
        output"""
        x1 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        with pytest.raises(np.linalg.LinAlgError):
            mlab.GaussianKDE(x1, "silverman")
