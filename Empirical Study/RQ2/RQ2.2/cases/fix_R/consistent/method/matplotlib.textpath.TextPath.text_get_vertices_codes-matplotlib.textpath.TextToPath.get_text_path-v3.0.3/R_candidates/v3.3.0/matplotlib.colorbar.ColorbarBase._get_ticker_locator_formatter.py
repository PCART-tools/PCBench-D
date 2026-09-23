    def _get_ticker_locator_formatter(self):
        """
        Return the ``locator`` and ``formatter`` of the colorbar.

        If they have not been defined (i.e. are *None*), suitable formatter
        and locator instances will be created, attached to the respective
        attributes and returned.
        """
        locator = self.locator
        formatter = self.formatter
        if locator is None:
            if self.boundaries is None:
                if isinstance(self.norm, colors.NoNorm):
                    nv = len(self._values)
                    base = 1 + int(nv / 10)
                    locator = ticker.IndexLocator(base=base, offset=0)
                elif isinstance(self.norm, colors.BoundaryNorm):
                    b = self.norm.boundaries
                    locator = ticker.FixedLocator(b, nbins=10)
                elif isinstance(self.norm, colors.LogNorm):
                    locator = _ColorbarLogLocator(self)
                elif isinstance(self.norm, colors.SymLogNorm):
                    # The subs setting here should be replaced
                    # by logic in the locator.
                    locator = ticker.SymmetricalLogLocator(
                                      subs=np.arange(1, 10),
                                      linthresh=self.norm.linthresh,
                                      base=10)
                else:
                    if mpl.rcParams['_internal.classic_mode']:
                        locator = ticker.MaxNLocator()
                    else:
                        locator = _ColorbarAutoLocator(self)
            else:
                b = self._boundaries[self._inside]
                locator = ticker.FixedLocator(b, nbins=10)

        if formatter is None:
            if isinstance(self.norm, colors.LogNorm):
                formatter = ticker.LogFormatterSciNotation()
            elif isinstance(self.norm, colors.SymLogNorm):
                formatter = ticker.LogFormatterSciNotation(
                                        linthresh=self.norm.linthresh)
            else:
                formatter = ticker.ScalarFormatter()
        else:
            formatter = self.formatter

        self.locator = locator
        self.formatter = formatter
        _log.debug('locator: %r', locator)
        return locator, formatter
