    def test_set_params(self):
        """
        Create null locator, and attempt to call set_params() on it.
        Should not exception, and should raise a warning.
        """
        loc = mticker.NullLocator()
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            loc.set_params()
            assert len(w) == 1
