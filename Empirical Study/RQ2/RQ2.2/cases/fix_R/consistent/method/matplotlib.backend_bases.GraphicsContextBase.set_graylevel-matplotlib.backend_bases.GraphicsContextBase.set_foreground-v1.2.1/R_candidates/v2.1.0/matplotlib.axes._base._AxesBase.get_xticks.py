    def get_xticks(self, minor=False):
        """Return the x ticks as a list of locations"""
        return self.xaxis.get_ticklocs(minor=minor)
