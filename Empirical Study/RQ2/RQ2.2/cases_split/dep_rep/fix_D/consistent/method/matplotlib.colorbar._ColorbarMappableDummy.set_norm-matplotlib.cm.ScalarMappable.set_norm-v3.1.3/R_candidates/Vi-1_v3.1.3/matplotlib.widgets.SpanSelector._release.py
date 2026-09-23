    def _release(self, event):
        """on button release event"""
        if self.pressv is None:
            return

        self.rect.set_visible(False)

        if self.span_stays:
            self.stay_rect.set_x(self.rect.get_x())
            self.stay_rect.set_y(self.rect.get_y())
            self.stay_rect.set_width(self.rect.get_width())
            self.stay_rect.set_height(self.rect.get_height())
            self.stay_rect.set_visible(True)

        self.canvas.draw_idle()
        vmin = self.pressv
        xdata, ydata = self._get_data(event)
        if self.direction == 'horizontal':
            vmax = xdata or self.prev[0]
        else:
            vmax = ydata or self.prev[1]

        if vmin > vmax:
            vmin, vmax = vmax, vmin
        span = vmax - vmin
        if self.minspan is not None and span < self.minspan:
            return
        self.onselect(vmin, vmax)
        self.pressv = None
        return False
