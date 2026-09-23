    def test_convert_float_array(self):
        data = np.array([1, 2, 3], dtype=float)
        with pytest.warns(MatplotlibDeprecationWarning):
            actual = self.cc.convert(data, self.unit, self.ax)
        np.testing.assert_allclose(actual, np.array([1., 2., 3.]))
