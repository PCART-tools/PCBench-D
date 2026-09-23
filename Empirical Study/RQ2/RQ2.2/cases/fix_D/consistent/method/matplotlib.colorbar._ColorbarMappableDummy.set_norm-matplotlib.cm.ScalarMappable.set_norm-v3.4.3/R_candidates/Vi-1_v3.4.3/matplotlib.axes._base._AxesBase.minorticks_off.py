    def minorticks_off(self):
        """Remove minor ticks from the axes."""
        self.xaxis.set_minor_locator(mticker.NullLocator())
        self.yaxis.set_minor_locator(mticker.NullLocator())
