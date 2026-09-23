    def update_ticks(self):
        """
        Force the update of the ticks and ticklabels. This must be
        called whenever the tick locator and/or tick formatter changes.
        """
        ax = self.ax
        # get the locator and formatter.  Defaults to
        # self.locator if not None..
        locator, formatter = self._get_ticker_locator_formatter()

        if self.orientation == 'vertical':
            long_axis, short_axis = ax.yaxis, ax.xaxis
        else:
            long_axis, short_axis = ax.xaxis, ax.yaxis

        if self._use_auto_colorbar_locator():
            _log.debug('Using auto colorbar locator on colorbar')
            _log.debug('locator: %r', locator)
            long_axis.set_major_locator(locator)
            long_axis.set_major_formatter(formatter)
            if type(self.norm) == colors.LogNorm:
                long_axis.set_minor_locator(_ColorbarLogLocator(self,
                            base=10., subs='auto'))
                long_axis.set_minor_formatter(
                    ticker.LogFormatter()
                )
        else:
            _log.debug('Using fixed locator on colorbar')
            ticks, ticklabels, offset_string = self._ticker(locator, formatter)
            long_axis.set_ticks(ticks)
            long_axis.set_ticklabels(ticklabels)
            long_axis.get_major_formatter().set_offset_string(offset_string)
