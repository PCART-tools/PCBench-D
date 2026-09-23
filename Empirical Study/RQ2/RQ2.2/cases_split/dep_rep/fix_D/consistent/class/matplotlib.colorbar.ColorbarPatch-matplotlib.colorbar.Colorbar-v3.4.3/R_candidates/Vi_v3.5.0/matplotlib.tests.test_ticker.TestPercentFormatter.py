class TestPercentFormatter:
    percent_data = [
        # Check explicitly set decimals over different intervals and values
        (100, 0, '%', 120, 100, '120%'),
        (100, 0, '%', 100, 90, '100%'),
        (100, 0, '%', 90, 50, '90%'),
        (100, 0, '%', -1.7, 40, '-2%'),
        (100, 1, '%', 90.0, 100, '90.0%'),
        (100, 1, '%', 80.1, 90, '80.1%'),
        (100, 1, '%', 70.23, 50, '70.2%'),
        # 60.554 instead of 60.55: see https://bugs.python.org/issue5118
        (100, 1, '%', -60.554, 40, '-60.6%'),
        # Check auto decimals over different intervals and values
        (100, None, '%', 95, 1, '95.00%'),
        (1.0, None, '%', 3, 6, '300%'),
        (17.0, None, '%', 1, 8.5, '6%'),
        (17.0, None, '%', 1, 8.4, '5.9%'),
        (5, None, '%', -100, 0.000001, '-2000.00000%'),
        # Check percent symbol
        (1.0, 2, None, 1.2, 100, '120.00'),
        (75, 3, '', 50, 100, '66.667'),
        (42, None, '^^Foobar$$', 21, 12, '50.0^^Foobar$$'),
    ]

    percent_ids = [
        # Check explicitly set decimals over different intervals and values
        'decimals=0, x>100%',
        'decimals=0, x=100%',
        'decimals=0, x<100%',
        'decimals=0, x<0%',
        'decimals=1, x>100%',
        'decimals=1, x=100%',
        'decimals=1, x<100%',
        'decimals=1, x<0%',
        # Check auto decimals over different intervals and values
        'autodecimal, x<100%, display_range=1',
        'autodecimal, x>100%, display_range=6 (custom xmax test)',
        'autodecimal, x<100%, display_range=8.5 (autodecimal test 1)',
        'autodecimal, x<100%, display_range=8.4 (autodecimal test 2)',
        'autodecimal, x<-100%, display_range=1e-6 (tiny display range)',
        # Check percent symbol
        'None as percent symbol',
        'Empty percent symbol',
        'Custom percent symbol',
    ]

    latex_data = [
        (False, False, r'50\{t}%'),
        (False, True, r'50\\\{t\}\%'),
        (True, False, r'50\{t}%'),
        (True, True, r'50\{t}%'),
    ]

    @pytest.mark.parametrize(
            'xmax, decimals, symbol, x, display_range, expected',
            percent_data, ids=percent_ids)
    def test_basic(self, xmax, decimals, symbol,
                   x, display_range, expected):
        formatter = mticker.PercentFormatter(xmax, decimals, symbol)
        with mpl.rc_context(rc={'text.usetex': False}):
            assert formatter.format_pct(x, display_range) == expected

    @pytest.mark.parametrize('is_latex, usetex, expected', latex_data)
    def test_latex(self, is_latex, usetex, expected):
        fmt = mticker.PercentFormatter(symbol='\\{t}%', is_latex=is_latex)
        with mpl.rc_context(rc={'text.usetex': usetex}):
            assert fmt.format_pct(50, 100) == expected
