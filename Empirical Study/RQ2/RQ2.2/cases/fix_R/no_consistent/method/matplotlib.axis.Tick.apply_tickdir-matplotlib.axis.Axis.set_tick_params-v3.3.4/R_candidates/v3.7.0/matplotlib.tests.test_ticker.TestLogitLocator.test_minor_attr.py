    def test_minor_attr(self):
        loc = mticker.LogitLocator(nbins=100)
        assert not loc.minor
        loc.minor = True
        assert loc.minor
        loc.set_params(minor=False)
        assert not loc.minor
