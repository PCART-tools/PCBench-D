    def set_ticklabels(self, ticklabels, update_ticks=True):
        """
        Set tick labels.

        Tick labels are updated immediately unless *update_ticks* is *False*,
        in which case one should call `.update_ticks` explicitly.
        """
        if isinstance(self.locator, ticker.FixedLocator):
            self.formatter = ticker.FixedFormatter(ticklabels)
            if update_ticks:
                self.update_ticks()
        else:
            cbook._warn_external("set_ticks() must have been called.")
        self.stale = True
