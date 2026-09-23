    def test_basic_with_offset(self):
        loc = mticker.MultipleLocator(base=3.147, offset=1.2)
        test_value = np.array([-8.241, -5.094, -1.947, 1.2, 4.347, 7.494,
                               10.641])
        assert_almost_equal(loc.tick_values(-7, 10), test_value)
