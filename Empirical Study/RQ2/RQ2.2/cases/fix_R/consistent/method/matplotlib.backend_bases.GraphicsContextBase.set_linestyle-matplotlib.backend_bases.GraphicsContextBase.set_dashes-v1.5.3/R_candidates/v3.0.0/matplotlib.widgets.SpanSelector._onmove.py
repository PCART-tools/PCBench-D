    def _onmove(self, event):
        """on motion notify event"""
        if self.pressv is None:
            return

        self._set_span_xy(event)

        if self.onmove_callback is not None:
            vmin = self.pressv
            xdata, ydata = self._get_data(event)
            if self.direction == 'horizontal':
                vmax = xdata or self.prev[0]
            else:
                vmax = ydata or self.prev[1]

            if vmin > vmax:
                vmin, vmax = vmax, vmin
            self.onmove_callback(vmin, vmax)

        self.update()
        return False
