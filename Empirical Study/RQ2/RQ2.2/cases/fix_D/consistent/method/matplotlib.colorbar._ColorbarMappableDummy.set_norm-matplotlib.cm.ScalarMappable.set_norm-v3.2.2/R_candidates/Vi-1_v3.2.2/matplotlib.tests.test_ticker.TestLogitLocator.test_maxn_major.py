    @pytest.mark.parametrize("lims", ref_maxn_limits)
    def test_maxn_major(self, lims):
        """
        When the axis is zoomed, the locator must have the same behavior as
        MaxNLocator.
        """
        loc = mticker.LogitLocator(nbins=100)
        maxn_loc = mticker.MaxNLocator(nbins=100, steps=[1, 2, 5, 10])
        for nbins in (4, 8, 16):
            loc.set_params(nbins=nbins)
            maxn_loc.set_params(nbins=nbins)
            ticks = loc.tick_values(*lims)
            maxn_ticks = maxn_loc.tick_values(*lims)
            assert ticks.shape == maxn_ticks.shape
            assert (ticks == maxn_ticks).all()
