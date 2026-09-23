    @pytest.mark.parametrize(
            'labelOnlyBase, exponent, locs, positions, expected', param_data)
    @pytest.mark.parametrize('base', base_data)
    def test_basic(self, labelOnlyBase, base, exponent, locs, positions,
                   expected):
        formatter = mticker.LogFormatterExponent(base=base,
                                                 labelOnlyBase=labelOnlyBase)
        formatter.axis = FakeAxis(1, base**exponent)
        vals = base**locs
        labels = [formatter(x, pos) for (x, pos) in zip(vals, positions)]
        expected = [label.replace('-', '\N{Minus Sign}') for label in expected]
        assert labels == expected
