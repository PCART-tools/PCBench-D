class TestLogitFormatter:
    @staticmethod
    def logit_deformatter(string):
        r"""
        Parser to convert string as r'$\mathdefault{1.41\cdot10^{-4}}$' in
        float 1.41e-4, as '0.5' or as r'$\mathdefault{\frac{1}{2}}$' in float
        0.5,
        """
        match = re.match(
            r"[^\d]*"
            r"(?P<comp>1-)?"
            r"(?P<mant>\d*\.?\d*)?"
            r"(?:\\cdot)?"
            r"(?:10\^\{(?P<expo>-?\d*)})?"
            r"[^\d]*$",
            string,
        )
        if match:
            comp = match["comp"] is not None
            mantissa = float(match["mant"]) if match["mant"] else 1
            expo = int(match["expo"]) if match["expo"] is not None else 0
            value = mantissa * 10 ** expo
            if match["mant"] or match["expo"] is not None:
                if comp:
                    return 1 - value
                return value
        match = re.match(
            r"[^\d]*\\frac\{(?P<num>\d+)\}\{(?P<deno>\d+)\}[^\d]*$", string
        )
        if match:
            num, deno = float(match["num"]), float(match["deno"])
            return num / deno
        raise ValueError("Not formatted by LogitFormatter")

    @pytest.mark.parametrize(
        "fx, x",
        [
            (r"STUFF0.41OTHERSTUFF", 0.41),
            (r"STUFF1.41\cdot10^{-2}OTHERSTUFF", 1.41e-2),
            (r"STUFF1-0.41OTHERSTUFF", 1 - 0.41),
            (r"STUFF1-1.41\cdot10^{-2}OTHERSTUFF", 1 - 1.41e-2),
            (r"STUFF", None),
            (r"STUFF12.4e-3OTHERSTUFF", None),
        ],
    )
    def test_logit_deformater(self, fx, x):
        if x is None:
            with pytest.raises(ValueError):
                TestLogitFormatter.logit_deformatter(fx)
        else:
            y = TestLogitFormatter.logit_deformatter(fx)
            assert _LogitHelper.isclose(x, y)

    decade_test = sorted(
        [10 ** (-i) for i in range(1, 10)]
        + [1 - 10 ** (-i) for i in range(1, 10)]
        + [1 / 2]
    )

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

    @pytest.mark.parametrize("x", 1 / (1 + np.exp(-np.linspace(-7, 7, 10))))
    def test_variablelength(self, x):
        """
        The format length should change depending on the neighbor labels.
        """
        formatter = mticker.LogitFormatter(use_overline=False)
        for N in (10, 20, 50, 100, 200, 1000, 2000, 5000, 10000):
            if x + 1 / N < 1:
                formatter.set_locs([x - 1 / N, x, x + 1 / N])
                sx = formatter(x)
                sx1 = formatter(x + 1 / N)
                d = (
                    TestLogitFormatter.logit_deformatter(sx1)
                    - TestLogitFormatter.logit_deformatter(sx)
                )
                assert 0 < d < 2 / N

    lims_minor_major = [
        (True, (5e-8, 1 - 5e-8), ((25, False), (75, False))),
        (True, (5e-5, 1 - 5e-5), ((25, False), (75, True))),
        (True, (5e-2, 1 - 5e-2), ((25, True), (75, True))),
        (False, (0.75, 0.76, 0.77), ((7, True), (25, True), (75, True))),
    ]

    @pytest.mark.parametrize("method, lims, cases", lims_minor_major)
    def test_minor_vs_major(self, method, lims, cases):
        """
        Test minor/major displays.
        """

        if method:
            min_loc = mticker.LogitLocator(minor=True)
            ticks = min_loc.tick_values(*lims)
        else:
            ticks = np.array(lims)
        min_form = mticker.LogitFormatter(minor=True)
        for threshold, has_minor in cases:
            min_form.set_minor_threshold(threshold)
            formatted = min_form.format_ticks(ticks)
            labelled = [f for f in formatted if len(f) > 0]
            if has_minor:
                assert len(labelled) > 0, (threshold, has_minor)
            else:
                assert len(labelled) == 0, (threshold, has_minor)

    def test_minor_number(self):
        """
        Test the parameter minor_number
        """
        min_loc = mticker.LogitLocator(minor=True)
        min_form = mticker.LogitFormatter(minor=True)
        ticks = min_loc.tick_values(5e-2, 1 - 5e-2)
        for minor_number in (2, 4, 8, 16):
            min_form.set_minor_number(minor_number)
            formatted = min_form.format_ticks(ticks)
            labelled = [f for f in formatted if len(f) > 0]
            assert len(labelled) == minor_number

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

    def test_one_half(self):
        """
        Test the parameter one_half
        """
        form = mticker.LogitFormatter()
        assert r"\frac{1}{2}" in form(1/2)
        form.set_one_half("1/2")
        assert "1/2" in form(1/2)
        form.set_one_half("one half")
        assert "one half" in form(1/2)

    @pytest.mark.parametrize("N", (100, 253, 754))
    def test_format_data_short(self, N):
        locs = np.linspace(0, 1, N)[1:-1]
        form = mticker.LogitFormatter()
        for x in locs:
            fx = form.format_data_short(x)
            if fx.startswith("1-"):
                x2 = 1 - float(fx[2:])
            else:
                x2 = float(fx)
            assert abs(x - x2) < 1 / N
