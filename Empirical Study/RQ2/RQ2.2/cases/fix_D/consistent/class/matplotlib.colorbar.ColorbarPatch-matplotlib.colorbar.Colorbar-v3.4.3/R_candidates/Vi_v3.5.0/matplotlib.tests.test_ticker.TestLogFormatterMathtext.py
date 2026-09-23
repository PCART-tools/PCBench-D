class TestLogFormatterMathtext:
    fmt = mticker.LogFormatterMathtext()
    test_data = [
        (0, 1, '$\\mathdefault{10^{0}}$'),
        (0, 1e-2, '$\\mathdefault{10^{-2}}$'),
        (0, 1e2, '$\\mathdefault{10^{2}}$'),
        (3, 1, '$\\mathdefault{1}$'),
        (3, 1e-2, '$\\mathdefault{0.01}$'),
        (3, 1e2, '$\\mathdefault{100}$'),
        (3, 1e-3, '$\\mathdefault{10^{-3}}$'),
        (3, 1e3, '$\\mathdefault{10^{3}}$'),
    ]

    @pytest.mark.parametrize('min_exponent, value, expected', test_data)
    def test_min_exponent(self, min_exponent, value, expected):
        with mpl.rc_context({'axes.formatter.min_exponent': min_exponent}):
            assert self.fmt(value) == expected
