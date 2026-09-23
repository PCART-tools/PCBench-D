    def view_limits(self, vmin, vmax):
        'Try to choose the view limits intelligently'

        d = abs(vmax - vmin)
        self._locator = self.get_locator(d)
        return self._locator.view_limits(vmin, vmax)
