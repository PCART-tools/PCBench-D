    @pytest.mark.parametrize(
            'xmax, decimals, symbol, x, display_range, expected',
            percent_data, ids=percent_ids)
    def test_basic(self, xmax, decimals, symbol,
                   x, display_range, expected):
        formatter = mticker.PercentFormatter(xmax, decimals, symbol)
        with matplotlib.rc_context(rc={'text.usetex': False}):
            assert formatter.format_pct(x, display_range) == expected
