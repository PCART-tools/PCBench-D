    def test_basic(self):
        loc = mticker.MultipleLocator(base=3.147)
        test_value = np.array([-9.441, -6.294, -3.147, 0., 3.147, 6.294,
                               9.441, 12.588])
        assert_almost_equal(loc.tick_values(-7, 10), test_value)
