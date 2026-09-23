    def test_evaluate_dim_and_num(self):
        """Tests if evaluated against a one by one array"""
        x1 = np.arange(3, 10, 2)
        x2 = np.array([3])
        kde = mlab.GaussianKDE(x1)
        y_expected = [0.08797252]
        y = kde.evaluate(x2)
        np.testing.assert_array_almost_equal(y, y_expected, 7)
