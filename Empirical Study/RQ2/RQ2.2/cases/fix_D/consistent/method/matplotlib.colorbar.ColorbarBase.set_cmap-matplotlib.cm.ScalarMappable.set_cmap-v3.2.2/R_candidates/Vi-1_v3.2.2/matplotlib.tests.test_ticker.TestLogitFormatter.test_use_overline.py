    def test_use_overline(self):
        """
        Test the parameter use_overline
        """
        x = 1 - 1e-2
        fx1 = r"$\mathdefault{1-10^{-2}}$"
        fx2 = r"$\mathdefault{\overline{10^{-2}}}$"
        form = mticker.LogitFormatter(use_overline=False)
        assert form(x) == fx1
        form.use_overline(True)
        assert form(x) == fx2
        form.use_overline(False)
        assert form(x) == fx1
