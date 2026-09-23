class TestFixedLocator:
    def test_set_params(self):
        """
        Create fixed locator with 5 nbins, and change it to something else.
        See if change was successful.
        Should not exception.
        """
        fixed = mticker.FixedLocator(range(0, 24), nbins=5)
        fixed.set_params(nbins=7)
        assert fixed.nbins == 7
