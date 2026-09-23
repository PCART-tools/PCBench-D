    def _update_pixel_ratio(self):
        if self._set_device_pixel_ratio(_devicePixelRatioF(self)):
            # The easiest way to resize the canvas is to emit a resizeEvent
            # since we implement all the logic for resizing the canvas for
            # that event.
            event = QtGui.QResizeEvent(self.size(), self.size())
            self.resizeEvent(event)
