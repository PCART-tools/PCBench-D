class TestStrMethodFormatter:
    test_data = [
        ('{x:05d}', (2,), '00002'),
        ('{x:03d}-{pos:02d}', (2, 1), '002-01'),
    ]

    @pytest.mark.parametrize('format, input, expected', test_data)
    def test_basic(self, format, input, expected):
        fmt = mticker.StrMethodFormatter(format)
        assert fmt(*input) == expected
