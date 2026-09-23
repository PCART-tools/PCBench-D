    def set_axis(self, axis):
        self._wrapped_locator.set_axis(axis)
        return super().set_axis(axis)
