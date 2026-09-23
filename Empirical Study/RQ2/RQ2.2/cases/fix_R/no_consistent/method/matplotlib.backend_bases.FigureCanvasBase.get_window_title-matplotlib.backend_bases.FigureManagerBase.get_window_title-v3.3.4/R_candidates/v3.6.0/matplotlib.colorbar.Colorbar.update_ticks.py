    def update_ticks(self):
        """
        Setup the ticks and ticklabels. This should not be needed by users.
        """
        # Get the locator and formatter; defaults to self._locator if not None.
        self._get_ticker_locator_formatter()
        self._long_axis().set_major_locator(self._locator)
        self._long_axis().set_minor_locator(self._minorlocator)
        self._long_axis().set_major_formatter(self._formatter)
