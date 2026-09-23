    def test_scott_multidim_dataset(self):
        """Test scott's output for a multi-dimensional array."""
        x1 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        with pytest.raises(np.linalg.LinAlgError):
            mlab.GaussianKDE(x1, "scott")
