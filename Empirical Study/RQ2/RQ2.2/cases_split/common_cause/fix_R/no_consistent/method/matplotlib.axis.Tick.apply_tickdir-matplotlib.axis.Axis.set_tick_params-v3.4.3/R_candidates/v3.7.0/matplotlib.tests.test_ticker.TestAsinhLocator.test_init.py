    def test_init(self):
        lctr = mticker.AsinhLocator(linear_width=2.718, numticks=19)
        assert lctr.linear_width == 2.718
        assert lctr.numticks == 19
        assert lctr.base == 10
