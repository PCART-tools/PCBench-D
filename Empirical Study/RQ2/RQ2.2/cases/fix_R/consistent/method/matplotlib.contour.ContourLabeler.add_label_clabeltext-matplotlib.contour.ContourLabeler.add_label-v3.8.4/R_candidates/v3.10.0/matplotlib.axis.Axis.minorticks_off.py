    def minorticks_off(self):
        """Remove minor ticks from the Axis."""
        self.set_minor_locator(mticker.NullLocator())
