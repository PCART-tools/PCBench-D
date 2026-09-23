    def test_wide_values(self):
        lctr = mticker.AsinhLocator(linear_width=0.1, numticks=11, base=0)

        assert_almost_equal(lctr.tick_values(-100, 100),
                            [-100, -20, -5, -1, -0.2,
                             0, 0.2, 1, 5, 20, 100])
        assert_almost_equal(lctr.tick_values(-1000, 1000),
                            [-1000, -100, -20, -3, -0.4,
                             0, 0.4, 3, 20, 100, 1000])
