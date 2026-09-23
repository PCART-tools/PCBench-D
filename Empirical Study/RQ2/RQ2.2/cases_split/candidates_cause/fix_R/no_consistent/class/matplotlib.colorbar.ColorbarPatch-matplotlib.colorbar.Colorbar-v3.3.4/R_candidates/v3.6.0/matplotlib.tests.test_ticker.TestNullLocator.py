class TestNullLocator:
    def test_set_params(self):
        """
        Create null locator, and attempt to call set_params() on it.
        Should not exception, and should raise a warning.
        """
        loc = mticker.NullLocator()
        with pytest.warns(UserWarning):
            loc.set_params()
