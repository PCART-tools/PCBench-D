    @pytest.mark.parametrize('vmin, vmax, steps, expected', integer_data)
    def test_integer(self, vmin, vmax, steps, expected):
        loc = mticker.MaxNLocator(nbins=5, integer=True, steps=steps)
        assert_almost_equal(loc.tick_values(vmin, vmax), expected)
