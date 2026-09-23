    def view_limits(self, vmin, vmax):
        """Try to choose the view limits intelligently."""
        b = self._base

        vmin, vmax = self.nonsingular(vmin, vmax)

        if self.axis.axes.name == 'polar':
            vmax = math.ceil(math.log(vmax) / math.log(b))
            vmin = b ** (vmax - self.numdecs)

        if mpl.rcParams['axes.autolimit_mode'] == 'round_numbers':
            vmin = _decade_less_equal(vmin, self._base)
            vmax = _decade_greater_equal(vmax, self._base)

        return vmin, vmax
