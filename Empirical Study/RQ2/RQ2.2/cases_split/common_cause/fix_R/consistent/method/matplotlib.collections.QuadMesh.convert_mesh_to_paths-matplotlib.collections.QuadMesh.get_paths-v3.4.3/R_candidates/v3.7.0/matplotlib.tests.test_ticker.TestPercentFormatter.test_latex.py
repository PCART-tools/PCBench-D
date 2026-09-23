    @pytest.mark.parametrize('is_latex, usetex, expected', latex_data)
    def test_latex(self, is_latex, usetex, expected):
        fmt = mticker.PercentFormatter(symbol='\\{t}%', is_latex=is_latex)
        with mpl.rc_context(rc={'text.usetex': usetex}):
            assert fmt.format_pct(50, 100) == expected
