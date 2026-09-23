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
