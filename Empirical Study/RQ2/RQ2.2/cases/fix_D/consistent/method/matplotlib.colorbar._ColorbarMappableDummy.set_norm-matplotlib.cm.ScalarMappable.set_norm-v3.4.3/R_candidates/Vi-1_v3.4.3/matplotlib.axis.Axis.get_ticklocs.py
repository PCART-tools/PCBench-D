    @_api.make_keyword_only("3.3", "minor")
    def get_ticklocs(self, minor=False):
        """Return this Axis' tick locations in data coordinates."""
        return self.get_minorticklocs() if minor else self.get_majorticklocs()
