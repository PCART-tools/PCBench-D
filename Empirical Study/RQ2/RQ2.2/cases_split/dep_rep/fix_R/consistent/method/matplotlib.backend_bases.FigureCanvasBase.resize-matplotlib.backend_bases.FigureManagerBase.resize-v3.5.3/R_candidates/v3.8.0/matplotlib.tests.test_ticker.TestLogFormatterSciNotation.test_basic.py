    @mpl.style.context('default')
    @pytest.mark.parametrize('base, value, expected', test_data)
    def test_basic(self, base, value, expected):
        formatter = mticker.LogFormatterSciNotation(base=base)
        with mpl.rc_context({'text.usetex': False}):
            assert formatter(value) == expected
