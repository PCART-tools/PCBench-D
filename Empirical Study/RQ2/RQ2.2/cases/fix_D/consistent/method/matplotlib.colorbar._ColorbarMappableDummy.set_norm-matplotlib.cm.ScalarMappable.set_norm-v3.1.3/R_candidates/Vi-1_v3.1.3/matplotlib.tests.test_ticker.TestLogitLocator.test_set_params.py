    def test_set_params(self):
        """
        Create logit locator with default minor=False, and change it to
        something else. See if change was successful. Should not exception.
        """
        loc = mticker.LogitLocator()  # Defaults to false.
        loc.set_params(minor=True)
        assert loc.minor
