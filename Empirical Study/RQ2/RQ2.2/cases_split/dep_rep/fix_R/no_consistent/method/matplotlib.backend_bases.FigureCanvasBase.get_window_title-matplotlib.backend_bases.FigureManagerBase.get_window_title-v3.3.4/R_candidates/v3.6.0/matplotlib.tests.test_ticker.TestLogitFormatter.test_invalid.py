    @pytest.mark.parametrize("x", (-1, -0.5, -0.1, 1.1, 1.5, 2))
    def test_invalid(self, x):
        """
        Test that invalid value are formatted with empty string without
        raising exception.
        """
        formatter = mticker.LogitFormatter(use_overline=False)
        formatter.set_locs(self.decade_test)
        s = formatter(x)
        assert s == ""
