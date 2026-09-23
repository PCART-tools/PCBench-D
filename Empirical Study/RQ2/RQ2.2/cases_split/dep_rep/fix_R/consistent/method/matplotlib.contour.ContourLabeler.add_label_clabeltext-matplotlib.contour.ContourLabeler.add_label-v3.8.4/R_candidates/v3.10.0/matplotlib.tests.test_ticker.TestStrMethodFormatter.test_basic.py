    @pytest.mark.parametrize('format, input, unicode_minus, expected', test_data)
    def test_basic(self, format, input, unicode_minus, expected):
        with mpl.rc_context({"axes.unicode_minus": unicode_minus}):
            fmt = mticker.StrMethodFormatter(format)
            assert fmt(*input) == expected
