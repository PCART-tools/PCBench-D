    @locator.setter
    def locator(self, locator):
        if not isinstance(locator, mticker.Locator):
            raise TypeError('locator must be a subclass of '
                            'matplotlib.ticker.Locator')
        self._locator = locator
