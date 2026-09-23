    def set_data_interval(self, vmin, vmax):
        self._wrapped_locator.set_data_interval(vmin, vmax)
        return super().set_data_interval(vmin, vmax)
