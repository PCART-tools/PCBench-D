    @cbook.deprecated("3.3")
    def pan(self, numsteps):
        """Pan by *numsteps* (can be positive or negative)."""
        self.major.locator.pan(numsteps)
