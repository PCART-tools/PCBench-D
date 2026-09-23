    @cbook._make_keyword_only("3.2", "minor")
    def get_yticks(self, minor=False):
        """Return the y ticks as a list of locations"""
        return self.yaxis.get_ticklocs(minor=minor)
