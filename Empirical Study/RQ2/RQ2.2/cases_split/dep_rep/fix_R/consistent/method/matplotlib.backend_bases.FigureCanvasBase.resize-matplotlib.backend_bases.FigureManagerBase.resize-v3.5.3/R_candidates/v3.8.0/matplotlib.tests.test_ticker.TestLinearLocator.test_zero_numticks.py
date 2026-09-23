    def test_zero_numticks(self):
        loc = mticker.LinearLocator(numticks=0)
        loc.tick_values(-0.8, 0.2) == []
