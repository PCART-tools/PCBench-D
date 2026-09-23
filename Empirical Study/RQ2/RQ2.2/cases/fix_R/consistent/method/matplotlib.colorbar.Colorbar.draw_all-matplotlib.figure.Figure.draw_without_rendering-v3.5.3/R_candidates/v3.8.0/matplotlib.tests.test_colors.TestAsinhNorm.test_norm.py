    def test_norm(self):
        norm = mcolors.AsinhNorm(2, vmin=-4, vmax=4)
        vals = np.arange(-3.5, 3.5, 10)
        normed_vals = norm(vals)
        asinh2 = np.arcsinh(2)

        expected = (2 * np.arcsinh(vals / 2) + 2 * asinh2) / (4 * asinh2)
        assert_array_almost_equal(normed_vals, expected)
