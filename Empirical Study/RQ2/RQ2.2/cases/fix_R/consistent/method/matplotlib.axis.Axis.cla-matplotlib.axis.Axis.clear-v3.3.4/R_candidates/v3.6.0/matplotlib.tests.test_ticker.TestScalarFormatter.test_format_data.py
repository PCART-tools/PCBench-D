    @pytest.mark.parametrize('value, expected', format_data)
    def test_format_data(self, value, expected):
        mpl.rcParams['axes.unicode_minus'] = False
        sf = mticker.ScalarFormatter()
        assert sf.format_data(value) == expected
