    def _onMouseWheel(self, event):
        """Translate mouse wheel events into matplotlib events"""
        # Determine mouse location
        x = event.GetX()
        y = self.figure.bbox.height - event.GetY()
        # Convert delta/rotation/rate into a floating point step size
        step = event.LinesPerAction * event.WheelRotation / event.WheelDelta
        # Done handling event
        event.Skip()
        # Mac gives two events for every wheel event; skip every second one.
        if wx.Platform == '__WXMAC__':
            if not hasattr(self, '_skipwheelevent'):
                self._skipwheelevent = True
            elif self._skipwheelevent:
                self._skipwheelevent = False
                return  # Return without processing event
            else:
                self._skipwheelevent = True
        FigureCanvasBase.scroll_event(self, x, y, step, guiEvent=event)
