    def _update_pixel_ratio(self):
        # We need to be careful in cases with mixed resolution displays if
        # dpi_ratio changes.
        if self._dpi_ratio != self._dpi_ratio_prev:
            # We need to update the figure DPI.
            self._update_figure_dpi()
            self._dpi_ratio_prev = self._dpi_ratio
            # The easiest way to resize the canvas is to emit a resizeEvent
            # since we implement all the logic for resizing the canvas for
            # that event.
            event = QtGui.QResizeEvent(self.size(), self.size())
            self.resizeEvent(event)
