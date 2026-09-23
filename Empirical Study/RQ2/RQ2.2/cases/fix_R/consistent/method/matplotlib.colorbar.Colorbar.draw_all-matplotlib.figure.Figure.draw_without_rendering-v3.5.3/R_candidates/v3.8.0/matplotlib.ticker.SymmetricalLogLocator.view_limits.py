    def view_limits(self, vmin, vmax):
        """Try to choose the view limits intelligently."""
        b = self._base
        if vmax < vmin:
            vmin, vmax = vmax, vmin

        if mpl.rcParams['axes.autolimit_mode'] == 'round_numbers':
            vmin = _decade_less_equal(vmin, b)
            vmax = _decade_greater_equal(vmax, b)
            if vmin == vmax:
                vmin = _decade_less(vmin, b)
                vmax = _decade_greater(vmax, b)

        return mtransforms.nonsingular(vmin, vmax)
