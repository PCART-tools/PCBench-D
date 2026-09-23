    def test_view_limits(self):
        """
        Test basic behavior of view limits.
        """
        with matplotlib.rc_context({'axes.autolimit_mode': 'data'}):
            loc = mticker.MultipleLocator(base=3.147)
            assert_almost_equal(loc.view_limits(-5, 5), (-5, 5))
