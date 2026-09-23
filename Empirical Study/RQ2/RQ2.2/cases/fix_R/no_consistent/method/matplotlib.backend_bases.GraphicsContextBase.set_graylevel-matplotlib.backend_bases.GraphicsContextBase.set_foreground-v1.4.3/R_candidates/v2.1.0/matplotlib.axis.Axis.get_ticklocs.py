    def get_ticklocs(self, minor=False):
        "Get the tick locations in data coordinates as a numpy array"
        if minor:
            return self.minor.locator()
        return self.major.locator()
