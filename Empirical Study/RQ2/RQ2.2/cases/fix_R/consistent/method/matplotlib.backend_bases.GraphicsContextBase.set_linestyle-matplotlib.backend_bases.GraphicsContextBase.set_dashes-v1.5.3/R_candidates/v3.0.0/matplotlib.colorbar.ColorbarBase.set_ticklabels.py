    def set_ticklabels(self, ticklabels, update_ticks=True):
        """
        set tick labels. Tick labels are updated immediately unless
        update_ticks is *False*. To manually update the ticks, call
        *update_ticks* method explicitly.
        """
        if isinstance(self.locator, ticker.FixedLocator):
            self.formatter = ticker.FixedFormatter(ticklabels)
            if update_ticks:
                self.update_ticks()
        else:
            warnings.warn("set_ticks() must have been called.")
        self.stale = True
