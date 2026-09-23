    def resizeEvent(self, event):
        if self._in_resize_event:  # Prevent PyQt6 recursion
            return
        if self.figure is None:
            return
        self._in_resize_event = True
        try:
            w = event.size().width() * self.device_pixel_ratio
            h = event.size().height() * self.device_pixel_ratio
            dpival = self.figure.dpi
            winch = w / dpival
            hinch = h / dpival
            self.figure.set_size_inches(winch, hinch, forward=False)
            # pass back into Qt to let it finish
            QtWidgets.QWidget.resizeEvent(self, event)
            # emit our resize events
            ResizeEvent("resize_event", self)._process()
            self.draw_idle()
        finally:
            self._in_resize_event = False
