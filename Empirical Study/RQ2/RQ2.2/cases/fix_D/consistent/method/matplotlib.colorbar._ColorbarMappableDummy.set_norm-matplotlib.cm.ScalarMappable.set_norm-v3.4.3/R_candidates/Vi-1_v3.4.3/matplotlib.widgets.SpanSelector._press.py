    def _press(self, event):
        """Button press event handler."""
        self.rect.set_visible(self.visible)
        if self.span_stays:
            self.stay_rect.set_visible(False)
            # really force a draw so that the stay rect is not in
            # the blit background
            if self.useblit:
                self.canvas.draw()
        xdata, ydata = self._get_data(event)
        if self.direction == 'horizontal':
            self.pressv = xdata
        else:
            self.pressv = ydata

        self._set_span_xy(event)
        return False
