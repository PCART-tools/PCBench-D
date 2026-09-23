    @pytest.mark.parametrize('input, expected', raw_format_data)
    def test_params(self, input, expected):
        """
        Test the formatting of EngFormatter for various values of the 'places'
        argument, in several cases:
            0. without a unit symbol but with a (default) space separator;
            1. with both a unit symbol and a (default) space separator;
            2. with both a unit symbol and some non default separators;
            3. without a unit symbol but with some non default separators.
        Note that cases 2. and 3. are looped over several separator strings.
        """

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
