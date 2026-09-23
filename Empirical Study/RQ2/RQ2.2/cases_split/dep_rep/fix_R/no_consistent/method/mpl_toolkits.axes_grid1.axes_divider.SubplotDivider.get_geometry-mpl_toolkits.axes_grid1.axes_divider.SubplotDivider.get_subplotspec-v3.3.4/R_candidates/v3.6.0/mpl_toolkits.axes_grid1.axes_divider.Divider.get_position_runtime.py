    def get_position_runtime(self, ax, renderer):
        if self._locator is None:
            return self.get_position()
        else:
            return self._locator(ax, renderer).bounds
