    def _update_dpi(self):
        # As described in __init__ above, we need to be careful in cases with
        # mixed resolution displays if dpi_ratio is changing between painting
        # events.
        # Return whether we triggered a resizeEvent (and thus a paintEvent)
        # from within this function.
        if self._dpi_ratio != self._dpi_ratio_prev:
            # We need to update the figure DPI.
            self._update_figure_dpi()
            self._dpi_ratio_prev = self._dpi_ratio
            # The easiest way to resize the canvas is to emit a resizeEvent
            # since we implement all the logic for resizing the canvas for
            # that event.
            event = QtGui.QResizeEvent(self.size(), self.size())
            self.resizeEvent(event)
            # resizeEvent triggers a paintEvent itself, so we exit this one
            # (after making sure that the event is immediately handled).
            return True
        return False
