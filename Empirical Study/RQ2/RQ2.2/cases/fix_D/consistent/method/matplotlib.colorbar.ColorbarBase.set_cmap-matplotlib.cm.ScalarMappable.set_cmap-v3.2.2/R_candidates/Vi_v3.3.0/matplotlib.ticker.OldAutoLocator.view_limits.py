    def view_limits(self, vmin, vmax):
        # docstring inherited
        d = abs(vmax - vmin)
        locator = self.get_locator(d)
        return locator.view_limits(vmin, vmax)
