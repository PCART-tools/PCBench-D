    @pytest.mark.parametrize('vmin, vmax, expected', basic_data)
    def test_basic(self, vmin, vmax, expected):
        loc = mticker.MaxNLocator(nbins=5)
        assert_almost_equal(loc.tick_values(vmin, vmax), expected)
