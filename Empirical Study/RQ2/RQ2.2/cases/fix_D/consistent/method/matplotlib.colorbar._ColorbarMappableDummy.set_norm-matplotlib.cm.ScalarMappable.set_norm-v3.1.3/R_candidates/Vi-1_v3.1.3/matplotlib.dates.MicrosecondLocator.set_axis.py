    def set_axis(self, axis):
        self._wrapped_locator.set_axis(axis)
        return DateLocator.set_axis(self, axis)
