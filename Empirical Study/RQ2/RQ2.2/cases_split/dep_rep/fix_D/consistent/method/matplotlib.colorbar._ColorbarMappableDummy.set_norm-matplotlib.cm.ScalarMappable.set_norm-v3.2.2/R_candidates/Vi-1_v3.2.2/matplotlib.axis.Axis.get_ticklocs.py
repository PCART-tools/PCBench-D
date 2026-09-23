    def get_ticklocs(self, minor=False):
        """Get the array of tick locations in data coordinates."""
        return self.get_minorticklocs() if minor else self.get_majorticklocs()
