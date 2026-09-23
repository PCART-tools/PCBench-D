    def set_view_interval(self, vmin, vmax):
        self._wrapped_locator.set_view_interval(vmin, vmax)
        return DateLocator.set_view_interval(self, vmin, vmax)
