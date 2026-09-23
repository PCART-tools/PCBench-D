    def set_data_interval(self, vmin, vmax):
        self._wrapped_locator.set_data_interval(vmin, vmax)
        return DateLocator.set_data_interval(self, vmin, vmax)
