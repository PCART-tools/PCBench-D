    @pytest.mark.parametrize('value, domain, expected', pprint_data)
    def test_pprint(self, value, domain, expected):
        fmt = mticker.LogFormatter()
        label = fmt.pprint_val(value, domain)
        assert label == expected
