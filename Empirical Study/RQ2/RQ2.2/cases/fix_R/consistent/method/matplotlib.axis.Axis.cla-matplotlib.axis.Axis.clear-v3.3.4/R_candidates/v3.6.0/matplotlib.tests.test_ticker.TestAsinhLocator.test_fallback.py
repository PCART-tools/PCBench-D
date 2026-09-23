    def test_fallback(self):
        lctr = mticker.AsinhLocator(1.0, numticks=11)

        assert_almost_equal(lctr.tick_values(101, 102),
                            np.arange(101, 102.01, 0.1))
