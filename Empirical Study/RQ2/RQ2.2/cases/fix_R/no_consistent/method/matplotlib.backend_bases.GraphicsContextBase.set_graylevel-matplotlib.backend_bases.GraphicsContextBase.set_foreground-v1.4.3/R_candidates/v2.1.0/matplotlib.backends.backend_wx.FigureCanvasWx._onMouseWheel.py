    def _onMouseWheel(self, evt):
        """Translate mouse wheel events into matplotlib events"""

        # Determine mouse location
        x = evt.GetX()
        y = self.figure.bbox.height - evt.GetY()

        # Convert delta/rotation/rate into a floating point step size
        delta = evt.GetWheelDelta()
        rotation = evt.GetWheelRotation()
        rate = evt.GetLinesPerAction()
        # print "delta,rotation,rate",delta,rotation,rate
        step = rate * float(rotation) / delta

        # Done handling event
        evt.Skip()

        # Mac is giving two events for every wheel event
        # Need to skip every second one
        if wx.Platform == '__WXMAC__':
            if not hasattr(self, '_skipwheelevent'):
                self._skipwheelevent = True
            elif self._skipwheelevent:
                self._skipwheelevent = False
                return  # Return without processing event
            else:
                self._skipwheelevent = True

        # Convert to mpl event
        FigureCanvasBase.scroll_event(self, x, y, step, guiEvent=evt)
