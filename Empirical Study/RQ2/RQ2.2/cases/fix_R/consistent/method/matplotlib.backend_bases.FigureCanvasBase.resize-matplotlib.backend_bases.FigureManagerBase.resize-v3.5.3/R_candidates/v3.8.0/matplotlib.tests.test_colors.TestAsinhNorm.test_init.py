    def test_init(self):
        norm0 = mcolors.AsinhNorm()
        assert norm0.linear_width == 1

        norm5 = mcolors.AsinhNorm(linear_width=5)
        assert norm5.linear_width == 5
