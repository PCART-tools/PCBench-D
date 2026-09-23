    def test_switch_to_autolocator(self):
        loc = mticker.LogLocator(subs="all")
        assert_array_equal(loc.tick_values(0.45, 0.55),
                           [0.44, 0.46, 0.48, 0.5, 0.52, 0.54, 0.56])
        # check that we *skip* 1.0, and 10, because this is a minor locator
        loc = mticker.LogLocator(subs=np.arange(2, 10))
        assert 1.0 not in loc.tick_values(0.9, 20.)
        assert 10.0 not in loc.tick_values(0.9, 20.)
