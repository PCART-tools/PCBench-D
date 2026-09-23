    def _press(self, event):
        """on button press event"""
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
        return False
