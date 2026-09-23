    @pytest.mark.parametrize(
            'vmin, vmax, expected',
            [
                (0, 1, [0, 1]),
                (-1, 1, [-1, 0, 1]),
            ],
    )
    def test_values(self, vmin, vmax, expected):
        # https://github.com/matplotlib/matplotlib/issues/25945
        sym = mticker.SymmetricalLogLocator(base=10, linthresh=1)
        ticks = sym.tick_values(vmin=vmin, vmax=vmax)
        assert_array_equal(ticks, expected)
