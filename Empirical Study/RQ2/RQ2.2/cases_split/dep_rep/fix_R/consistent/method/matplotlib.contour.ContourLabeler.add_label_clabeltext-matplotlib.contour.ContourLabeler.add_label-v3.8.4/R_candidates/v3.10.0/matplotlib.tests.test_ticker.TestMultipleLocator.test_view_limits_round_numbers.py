    def test_view_limits_round_numbers(self):
        """
        Test that everything works properly with 'round_numbers' for auto
        limit.
        """
        with mpl.rc_context({'axes.autolimit_mode': 'round_numbers'}):
            loc = mticker.MultipleLocator(base=3.147)
            assert_almost_equal(loc.view_limits(-4, 4), (-6.294, 6.294))
