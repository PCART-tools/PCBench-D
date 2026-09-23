class TestScalarFormatter:
    offset_data = [
        (123, 189, 0),
        (-189, -123, 0),
        (12341, 12349, 12340),
        (-12349, -12341, -12340),
        (99999.5, 100010.5, 100000),
        (-100010.5, -99999.5, -100000),
        (99990.5, 100000.5, 100000),
        (-100000.5, -99990.5, -100000),
        (1233999, 1234001, 1234000),
        (-1234001, -1233999, -1234000),
        (1, 1, 1),
        (123, 123, 0),
        # Test cases courtesy of @WeatherGod
        (.4538, .4578, .45),
        (3789.12, 3783.1, 3780),
        (45124.3, 45831.75, 45000),
        (0.000721, 0.0007243, 0.00072),
        (12592.82, 12591.43, 12590),
        (9., 12., 0),
        (900., 1200., 0),
        (1900., 1200., 0),
        (0.99, 1.01, 1),
        (9.99, 10.01, 10),
        (99.99, 100.01, 100),
        (5.99, 6.01, 6),
        (15.99, 16.01, 16),
        (-0.452, 0.492, 0),
        (-0.492, 0.492, 0),
        (12331.4, 12350.5, 12300),
        (-12335.3, 12335.3, 0),
    ]

    use_offset_data = [True, False]

    #  (sci_type, scilimits, lim, orderOfMag, fewticks)
    scilimits_data = [
        (False, (0, 0), (10.0, 20.0), 0, False),
        (True, (-2, 2), (-10, 20), 0, False),
        (True, (-2, 2), (-20, 10), 0, False),
        (True, (-2, 2), (-110, 120), 2, False),
        (True, (-2, 2), (-120, 110), 2, False),
        (True, (-2, 2), (-.001, 0.002), -3, False),
        (True, (-7, 7), (0.18e10, 0.83e10), 9, True),
        (True, (0, 0), (-1e5, 1e5), 5, False),
        (True, (6, 6), (-1e5, 1e5), 6, False),
    ]

    cursor_data = [
        [0., "0.000"],
        [0.0123, "0.012"],
        [0.123, "0.123"],
        [1.23,  "1.230"],
        [12.3, "12.300"],
    ]

    @pytest.mark.parametrize('unicode_minus, result',
                             [(True, "\N{MINUS SIGN}1"), (False, "-1")])
    def test_unicode_minus(self, unicode_minus, result):
        mpl.rcParams['axes.unicode_minus'] = unicode_minus
        assert (
            plt.gca().xaxis.get_major_formatter().format_data_short(-1).strip()
            == result)

    @pytest.mark.parametrize('left, right, offset', offset_data)
    def test_offset_value(self, left, right, offset):
        fig, ax = plt.subplots()
        formatter = ax.xaxis.get_major_formatter()

        with (pytest.warns(UserWarning, match='Attempting to set identical')
              if left == right else nullcontext()):
            ax.set_xlim(left, right)
        ax.xaxis._update_ticks()
        assert formatter.offset == offset

        with (pytest.warns(UserWarning, match='Attempting to set identical')
              if left == right else nullcontext()):
            ax.set_xlim(right, left)
        ax.xaxis._update_ticks()
        assert formatter.offset == offset

    @pytest.mark.parametrize('use_offset', use_offset_data)
    def test_use_offset(self, use_offset):
        with mpl.rc_context({'axes.formatter.useoffset': use_offset}):
            tmp_form = mticker.ScalarFormatter()
            assert use_offset == tmp_form.get_useOffset()

    def test_use_locale(self):
        conv = locale.localeconv()
        sep = conv['thousands_sep']
        if not sep or conv['grouping'][-1:] in ([], [locale.CHAR_MAX]):
            pytest.skip('Locale does not apply grouping')  # pragma: no cover

        with mpl.rc_context({'axes.formatter.use_locale': True}):
            tmp_form = mticker.ScalarFormatter()
            assert tmp_form.get_useLocale()

            tmp_form.create_dummy_axis()
            tmp_form.set_bounds(0, 10)
            tmp_form.set_locs([1, 2, 3])
            assert sep in tmp_form(1e9)

    @pytest.mark.parametrize(
        'sci_type, scilimits, lim, orderOfMag, fewticks', scilimits_data)
    def test_scilimits(self, sci_type, scilimits, lim, orderOfMag, fewticks):
        tmp_form = mticker.ScalarFormatter()
        tmp_form.set_scientific(sci_type)
        tmp_form.set_powerlimits(scilimits)
        fig, ax = plt.subplots()
        ax.yaxis.set_major_formatter(tmp_form)
        ax.set_ylim(*lim)
        if fewticks:
            ax.yaxis.set_major_locator(mticker.MaxNLocator(4))

        tmp_form.set_locs(ax.yaxis.get_majorticklocs())
        assert orderOfMag == tmp_form.orderOfMagnitude

    @pytest.mark.parametrize('data, expected', cursor_data)
    def test_cursor_precision(self, data, expected):
        fig, ax = plt.subplots()
        ax.set_xlim(-1, 1)  # Pointing precision of 0.001.
        fmt = ax.xaxis.get_major_formatter().format_data_short
        assert fmt(data) == expected

    @pytest.mark.parametrize('data, expected', cursor_data)
    def test_cursor_dummy_axis(self, data, expected):
        # Issue #17624
        sf = mticker.ScalarFormatter()
        sf.create_dummy_axis()
        sf.set_bounds(0, 10)
        fmt = sf.format_data_short
        assert fmt(data) == expected
