    def test_evaluate_equal_dim_and_num_lt(self):
        """Test when line 3810 fails"""
        x1 = np.arange(3, 10, 2)
        x2 = np.arange(3, 8, 2)
        kde = mlab.GaussianKDE(x1)
        y_expected = [0.08797252, 0.11774109, 0.11774109]
        y = kde.evaluate(x2)
        np.testing.assert_array_almost_equal(y, y_expected, 7)
