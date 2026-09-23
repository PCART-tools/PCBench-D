    @_api.deprecated("3.5", alternative=".axis.set_view_interval")
    def set_view_interval(self, vmin, vmax):
        self.axis.set_view_interval(vmin, vmax)
