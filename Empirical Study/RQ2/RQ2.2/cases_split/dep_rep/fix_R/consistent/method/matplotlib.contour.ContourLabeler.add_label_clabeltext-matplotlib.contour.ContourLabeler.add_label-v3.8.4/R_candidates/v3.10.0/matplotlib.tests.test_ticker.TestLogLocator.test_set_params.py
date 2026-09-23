    def test_set_params(self):
        """
        Create log locator with default value, base=10.0, subs=[1.0],
        numticks=15 and change it to something else.
        See if change was successful. Should not raise exception.
        """
        loc = mticker.LogLocator()
        loc.set_params(numticks=7, subs=[2.0], base=4)
        assert loc.numticks == 7
        assert loc._base == 4
        assert list(loc._subs) == [2.0]
