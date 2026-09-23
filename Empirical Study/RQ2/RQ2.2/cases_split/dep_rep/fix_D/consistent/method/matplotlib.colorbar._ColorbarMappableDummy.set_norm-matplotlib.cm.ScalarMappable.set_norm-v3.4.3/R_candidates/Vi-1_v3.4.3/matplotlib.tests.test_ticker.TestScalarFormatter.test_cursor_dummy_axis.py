    @pytest.mark.parametrize('data, expected', cursor_data)
    def test_cursor_dummy_axis(self, data, expected):
        # Issue #17624
        sf = mticker.ScalarFormatter()
        sf.create_dummy_axis()
        sf.set_bounds(0, 10)
        fmt = sf.format_data_short
        assert fmt(data) == expected
