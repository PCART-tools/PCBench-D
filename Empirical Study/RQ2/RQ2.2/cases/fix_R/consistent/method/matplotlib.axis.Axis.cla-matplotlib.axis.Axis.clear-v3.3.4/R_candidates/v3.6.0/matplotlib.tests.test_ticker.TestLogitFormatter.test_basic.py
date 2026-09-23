    @pytest.mark.parametrize("x", decade_test)
    def test_basic(self, x):
        """
        Test the formatted value correspond to the value for ideal ticks in
        logit space.
        """
        formatter = mticker.LogitFormatter(use_overline=False)
        formatter.set_locs(self.decade_test)
        s = formatter(x)
        x2 = TestLogitFormatter.logit_deformatter(s)
        assert _LogitHelper.isclose(x, x2)
