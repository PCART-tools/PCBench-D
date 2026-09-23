    def test_basic(self):
        loc = mticker.LinearLocator(numticks=3)
        test_value = np.array([-0.8, -0.3, 0.2])
        assert_almost_equal(loc.tick_values(-0.8, 0.2), test_value)
