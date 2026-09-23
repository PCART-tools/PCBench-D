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
