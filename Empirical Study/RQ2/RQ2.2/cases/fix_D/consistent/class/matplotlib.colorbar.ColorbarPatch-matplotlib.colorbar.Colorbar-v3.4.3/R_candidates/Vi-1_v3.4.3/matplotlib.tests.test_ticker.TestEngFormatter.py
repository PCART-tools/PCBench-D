class TestEngFormatter:
    # (unicode_minus, input, expected) where ''expected'' corresponds to the
    # outputs respectively returned when (places=None, places=0, places=2)
    # unicode_minus is a boolean value for the rcParam['axes.unicode_minus']
    raw_format_data = [
        (False, -1234.56789, ('-1.23457 k', '-1 k', '-1.23 k')),
        (True, -1234.56789, ('\N{MINUS SIGN}1.23457 k', '\N{MINUS SIGN}1 k',
                             '\N{MINUS SIGN}1.23 k')),
        (False, -1.23456789, ('-1.23457', '-1', '-1.23')),
        (True, -1.23456789, ('\N{MINUS SIGN}1.23457', '\N{MINUS SIGN}1',
                             '\N{MINUS SIGN}1.23')),
        (False, -0.123456789, ('-123.457 m', '-123 m', '-123.46 m')),
        (True, -0.123456789, ('\N{MINUS SIGN}123.457 m', '\N{MINUS SIGN}123 m',
                              '\N{MINUS SIGN}123.46 m')),
        (False, -0.00123456789, ('-1.23457 m', '-1 m', '-1.23 m')),
        (True, -0.00123456789, ('\N{MINUS SIGN}1.23457 m', '\N{MINUS SIGN}1 m',
                                '\N{MINUS SIGN}1.23 m')),
        (True, -0.0, ('0', '0', '0.00')),
        (True, -0, ('0', '0', '0.00')),
        (True, 0, ('0', '0', '0.00')),
        (True, 1.23456789e-6, ('1.23457 µ', '1 µ', '1.23 µ')),
        (True, 0.123456789, ('123.457 m', '123 m', '123.46 m')),
        (True, 0.1, ('100 m', '100 m', '100.00 m')),
        (True, 1, ('1', '1', '1.00')),
        (True, 1.23456789, ('1.23457', '1', '1.23')),
        # places=0: corner-case rounding
        (True, 999.9, ('999.9', '1 k', '999.90')),
        # corner-case rounding for all
        (True, 999.9999, ('1 k', '1 k', '1.00 k')),
        # negative corner-case
        (False, -999.9999, ('-1 k', '-1 k', '-1.00 k')),
        (True, -999.9999, ('\N{MINUS SIGN}1 k', '\N{MINUS SIGN}1 k',
                           '\N{MINUS SIGN}1.00 k')),
        (True, 1000, ('1 k', '1 k', '1.00 k')),
        (True, 1001, ('1.001 k', '1 k', '1.00 k')),
        (True, 100001, ('100.001 k', '100 k', '100.00 k')),
        (True, 987654.321, ('987.654 k', '988 k', '987.65 k')),
        # OoR value (> 1000 Y)
        (True, 1.23e27, ('1230 Y', '1230 Y', '1230.00 Y'))
    ]

    @pytest.mark.parametrize('unicode_minus, input, expected', raw_format_data)
    def test_params(self, unicode_minus, input, expected):
        """
        Test the formatting of EngFormatter for various values of the 'places'
        argument, in several cases:

        0. without a unit symbol but with a (default) space separator;
        1. with both a unit symbol and a (default) space separator;
        2. with both a unit symbol and some non default separators;
        3. without a unit symbol but with some non default separators.

        Note that cases 2. and 3. are looped over several separator strings.
        """

        plt.rcParams['axes.unicode_minus'] = unicode_minus
        UNIT = 's'  # seconds
        DIGITS = '0123456789'  # %timeit showed 10-20% faster search than set

        # Case 0: unit='' (default) and sep=' ' (default).
        # 'expected' already corresponds to this reference case.
        exp_outputs = expected
        formatters = (
            mticker.EngFormatter(),  # places=None (default)
            mticker.EngFormatter(places=0),
            mticker.EngFormatter(places=2)
        )
        for _formatter, _exp_output in zip(formatters, exp_outputs):
            assert _formatter(input) == _exp_output

        # Case 1: unit=UNIT and sep=' ' (default).
        # Append a unit symbol to the reference case.
        # Beware of the values in [1, 1000), where there is no prefix!
        exp_outputs = (_s + " " + UNIT if _s[-1] in DIGITS  # case w/o prefix
                       else _s + UNIT for _s in expected)
        formatters = (
            mticker.EngFormatter(unit=UNIT),  # places=None (default)
            mticker.EngFormatter(unit=UNIT, places=0),
            mticker.EngFormatter(unit=UNIT, places=2)
        )
        for _formatter, _exp_output in zip(formatters, exp_outputs):
            assert _formatter(input) == _exp_output

        # Test several non default separators: no separator, a narrow
        # no-break space (unicode character) and an extravagant string.
        for _sep in ("", "\N{NARROW NO-BREAK SPACE}", "@_@"):
            # Case 2: unit=UNIT and sep=_sep.
            # Replace the default space separator from the reference case
            # with the tested one `_sep` and append a unit symbol to it.
            exp_outputs = (_s + _sep + UNIT if _s[-1] in DIGITS  # no prefix
                           else _s.replace(" ", _sep) + UNIT
                           for _s in expected)
            formatters = (
                mticker.EngFormatter(unit=UNIT, sep=_sep),  # places=None
                mticker.EngFormatter(unit=UNIT, places=0, sep=_sep),
                mticker.EngFormatter(unit=UNIT, places=2, sep=_sep)
            )
            for _formatter, _exp_output in zip(formatters, exp_outputs):
                assert _formatter(input) == _exp_output

            # Case 3: unit='' (default) and sep=_sep.
            # Replace the default space separator from the reference case
            # with the tested one `_sep`. Reference case is already unitless.
            exp_outputs = (_s.replace(" ", _sep) for _s in expected)
            formatters = (
                mticker.EngFormatter(sep=_sep),  # places=None (default)
                mticker.EngFormatter(places=0, sep=_sep),
                mticker.EngFormatter(places=2, sep=_sep)
            )
            for _formatter, _exp_output in zip(formatters, exp_outputs):
                assert _formatter(input) == _exp_output
