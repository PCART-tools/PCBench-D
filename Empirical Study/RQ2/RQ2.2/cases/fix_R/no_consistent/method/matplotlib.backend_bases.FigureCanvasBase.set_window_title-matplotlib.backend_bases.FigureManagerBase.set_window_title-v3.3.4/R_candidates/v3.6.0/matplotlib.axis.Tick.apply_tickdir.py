    @_api.deprecated("3.5", alternative="`.Axis.set_tick_params`")
    def apply_tickdir(self, tickdir):
        self._apply_tickdir(tickdir)
        self.stale = True
