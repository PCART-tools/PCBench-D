    @pytest.mark.parametrize('format, input, expected', test_data)
    def test_basic(self, format, input, expected):
        fmt = mticker.StrMethodFormatter(format)
        assert fmt(*input) == expected
