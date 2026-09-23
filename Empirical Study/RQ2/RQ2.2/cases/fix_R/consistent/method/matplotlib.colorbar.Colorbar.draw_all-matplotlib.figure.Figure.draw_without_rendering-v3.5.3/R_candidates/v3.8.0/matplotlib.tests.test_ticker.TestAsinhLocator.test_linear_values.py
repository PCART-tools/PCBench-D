    def test_linear_values(self):
        lctr = mticker.AsinhLocator(linear_width=100, numticks=11, base=0)

        assert_almost_equal(lctr.tick_values(-1, 1),
                            np.arange(-1, 1.01, 0.2))
        assert_almost_equal(lctr.tick_values(-0.1, 0.1),
                            np.arange(-0.1, 0.101, 0.02))
        assert_almost_equal(lctr.tick_values(-0.01, 0.01),
                            np.arange(-0.01, 0.0101, 0.002))
