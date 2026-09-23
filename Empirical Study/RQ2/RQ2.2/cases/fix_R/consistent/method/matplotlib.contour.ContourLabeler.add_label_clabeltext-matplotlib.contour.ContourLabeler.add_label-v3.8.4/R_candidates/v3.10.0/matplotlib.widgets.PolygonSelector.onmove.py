    def onmove(self, event):
        """Cursor move event handler and validator."""
        # Method overrides _SelectorWidget.onmove because the polygon selector
        # needs to process the move callback even if there is no button press.
        # _SelectorWidget.onmove include logic to ignore move event if
        # _eventpress is None.
        if self.ignore(event):
            # Hide the cursor when interactive zoom/pan is active
            if not self.canvas.widgetlock.available(self) and self._xys:
                self._xys[-1] = (np.nan, np.nan)
                self._draw_polygon()
            return False

        else:
            event = self._clean_event(event)
            self._onmove(event)
            return True
