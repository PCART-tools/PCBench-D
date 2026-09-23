    @pytest.mark.parametrize("okval", acceptable_vmin_vmax)
    def test_nonsingular_nok(self, okval):
        """
        Create logit locator, and test the nonsingular method for non
        acceptable value
        """
        loc = mticker.LogitLocator()
        vmin, vmax = (-1, okval)
        vmin2, vmax2 = loc.nonsingular(vmin, vmax)
        assert vmax2 == vmax
        assert 0 < vmin2 < vmax2
        vmin, vmax = (okval, 2)
        vmin2, vmax2 = loc.nonsingular(vmin, vmax)
        assert vmin2 == vmin
        assert vmin2 < vmax2 < 1
