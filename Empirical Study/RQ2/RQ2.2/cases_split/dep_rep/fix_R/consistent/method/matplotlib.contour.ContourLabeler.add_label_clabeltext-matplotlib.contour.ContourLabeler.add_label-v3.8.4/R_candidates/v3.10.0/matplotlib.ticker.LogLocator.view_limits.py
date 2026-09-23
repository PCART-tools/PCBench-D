    def view_limits(self, vmin, vmax):
        """Try to choose the view limits intelligently."""
        b = self._base

        vmin, vmax = self.nonsingular(vmin, vmax)

        if mpl.rcParams['axes.autolimit_mode'] == 'round_numbers':
            vmin = _decade_less_equal(vmin, b)
            vmax = _decade_greater_equal(vmax, b)

        return vmin, vmax
