    def test_view_limits_round_numbers_with_offset(self):
        """
        Test that everything works properly with 'round_numbers' for auto
        limit.
        """
        with mpl.rc_context({'axes.autolimit_mode': 'round_numbers'}):
            loc = mticker.MultipleLocator(base=3.147, offset=1.3)
            assert_almost_equal(loc.view_limits(-4, 4), (-4.994, 4.447))
