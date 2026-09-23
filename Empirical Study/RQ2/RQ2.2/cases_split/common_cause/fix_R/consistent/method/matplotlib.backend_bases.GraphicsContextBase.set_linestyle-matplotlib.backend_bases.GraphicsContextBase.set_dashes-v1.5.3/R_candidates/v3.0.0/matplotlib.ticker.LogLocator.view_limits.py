    def view_limits(self, vmin, vmax):
        'Try to choose the view limits intelligently'
        b = self._base

        vmin, vmax = self.nonsingular(vmin, vmax)

        if self.axis.axes.name == 'polar':
            vmax = math.ceil(math.log(vmax) / math.log(b))
            vmin = b ** (vmax - self.numdecs)

        if rcParams['axes.autolimit_mode'] == 'round_numbers':
            if not is_decade(vmin, self._base):
                vmin = decade_down(vmin, self._base)
            if not is_decade(vmax, self._base):
                vmax = decade_up(vmax, self._base)

        return vmin, vmax
