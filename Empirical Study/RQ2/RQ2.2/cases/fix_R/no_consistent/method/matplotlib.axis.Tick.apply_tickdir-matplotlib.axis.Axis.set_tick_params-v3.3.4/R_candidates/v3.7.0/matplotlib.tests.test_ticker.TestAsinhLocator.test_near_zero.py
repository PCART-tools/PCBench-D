    def test_near_zero(self):
        """Check that manually injected zero will supersede nearby tick"""
        lctr = mticker.AsinhLocator(linear_width=100, numticks=3, base=0)

        assert_almost_equal(lctr.tick_values(-1.1, 0.9), [-1.0, 0.0, 0.9])
