    def _on_mouse_wheel(self, event):
        """Translate mouse wheel events into matplotlib events"""
        x, y = self._mpl_coords(event)
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
        MouseEvent("scroll_event", self,
                   x, y, step=step, guiEvent=event)._process()
