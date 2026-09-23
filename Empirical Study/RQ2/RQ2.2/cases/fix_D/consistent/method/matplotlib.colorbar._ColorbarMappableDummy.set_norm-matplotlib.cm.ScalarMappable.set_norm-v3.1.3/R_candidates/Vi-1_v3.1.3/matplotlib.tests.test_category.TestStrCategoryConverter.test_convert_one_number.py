    def test_convert_one_number(self):
        actual = self.cc.convert(0.0, self.unit, self.ax)
        np.testing.assert_allclose(actual, np.array([0.]))
