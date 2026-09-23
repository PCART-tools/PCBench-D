    def test_base_rounding(self):
        lctr10 = mticker.AsinhLocator(linear_width=1, numticks=8,
                                      base=10, subs=(1, 3, 5))
        assert_almost_equal(lctr10.tick_values(-110, 110),
                            [-500, -300, -100, -50, -30, -10, -5, -3, -1,
                             -0.5, -0.3, -0.1, 0, 0.1, 0.3, 0.5,
                             1, 3, 5, 10, 30, 50, 100, 300, 500])

        lctr5 = mticker.AsinhLocator(linear_width=1, numticks=20, base=5)
        assert_almost_equal(lctr5.tick_values(-1050, 1050),
                            [-625, -125, -25, -5, -1, -0.2, 0,
                             0.2, 1, 5, 25, 125, 625])
