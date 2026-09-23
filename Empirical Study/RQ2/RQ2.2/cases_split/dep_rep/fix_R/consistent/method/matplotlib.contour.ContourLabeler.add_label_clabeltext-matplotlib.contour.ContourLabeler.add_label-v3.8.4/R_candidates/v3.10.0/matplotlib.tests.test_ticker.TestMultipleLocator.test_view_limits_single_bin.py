    def test_view_limits_single_bin(self):
        """
        Test that 'round_numbers' works properly with a single bin.
        """
        with mpl.rc_context({'axes.autolimit_mode': 'round_numbers'}):
            loc = mticker.MaxNLocator(nbins=1)
            assert_almost_equal(loc.view_limits(-2.3, 2.3), (-4, 4))
