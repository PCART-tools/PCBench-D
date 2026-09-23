    def test_convert_one_number(self):
        with pytest.warns(MatplotlibDeprecationWarning):
            actual = self.cc.convert(0.0, self.unit, self.ax)
        np.testing.assert_allclose(actual, np.array([0.]))
