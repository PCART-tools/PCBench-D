    @pytest.mark.parametrize('min_exponent, value, expected', test_data)
    def test_min_exponent(self, min_exponent, value, expected):
        with matplotlib.rc_context({'axes.formatter.min_exponent':
                                    min_exponent}):
            assert self.fmt(value) == expected
