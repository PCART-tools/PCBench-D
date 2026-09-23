    def test_per_subplot_kw_expander(self):
        normalize = Figure._norm_per_subplot_kw
        assert normalize({"A": {}, "B": {}}) == {"A": {}, "B": {}}
        assert normalize({("A", "B"): {}}) == {"A": {}, "B": {}}
        with pytest.raises(
                ValueError, match=f'The key {"B"!r} appears multiple times'
        ):
            normalize({("A", "B"): {}, "B": {}})
        with pytest.raises(
                ValueError, match=f'The key {"B"!r} appears multiple times'
        ):
            normalize({"B": {}, ("A", "B"): {}})
