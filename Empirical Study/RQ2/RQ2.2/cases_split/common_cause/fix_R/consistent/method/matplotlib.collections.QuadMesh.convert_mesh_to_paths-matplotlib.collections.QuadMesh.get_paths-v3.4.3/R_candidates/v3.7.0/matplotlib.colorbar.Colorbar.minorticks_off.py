    def minorticks_off(self):
        """Turn the minor ticks of the colorbar off."""
        self._minorlocator = ticker.NullLocator()
        self._long_axis().set_minor_locator(self._minorlocator)
