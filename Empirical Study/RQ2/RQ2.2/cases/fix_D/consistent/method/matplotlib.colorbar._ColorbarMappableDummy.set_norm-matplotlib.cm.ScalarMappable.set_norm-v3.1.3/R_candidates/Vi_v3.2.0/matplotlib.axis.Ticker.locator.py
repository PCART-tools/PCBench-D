    @locator.setter
    def locator(self, locator):
        if not isinstance(locator, mticker.Locator):
            cbook.warn_deprecated(
                "3.2", message="Support for locators that do not subclass "
                "matplotlib.ticker.Locator is deprecated since %(since)s and "
                "support for them will be removed %(removal)s.")
        self._locator = locator
