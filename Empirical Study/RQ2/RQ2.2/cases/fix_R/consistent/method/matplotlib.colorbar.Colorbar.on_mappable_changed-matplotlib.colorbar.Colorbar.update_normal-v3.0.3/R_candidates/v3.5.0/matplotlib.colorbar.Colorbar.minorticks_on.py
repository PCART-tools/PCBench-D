    def minorticks_on(self):
        """
        Turn on colorbar minor ticks.
        """
        self.ax.minorticks_on()
        self.minorlocator = self._long_axis().get_minor_locator()
        self._short_axis().set_minor_locator(ticker.NullLocator())
