    def get_yticks(self, minor=False):
        """Return the y ticks as a list of locations"""
        return self.yaxis.get_ticklocs(minor=minor)
