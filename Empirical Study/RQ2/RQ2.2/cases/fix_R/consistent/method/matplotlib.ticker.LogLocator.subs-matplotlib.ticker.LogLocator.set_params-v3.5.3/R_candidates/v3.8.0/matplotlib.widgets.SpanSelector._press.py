    def _press(self, event):
        """Button press event handler."""
        self._set_cursor(True)
        if self._interactive and self._selection_artist.get_visible():
            self._set_active_handle(event)
        else:
            self._active_handle = None

        if self._active_handle is None or not self._interactive:
            # Clear previous rectangle before drawing new rectangle.
            self.update()

        xdata, ydata = self._get_data_coords(event)
        v = xdata if self.direction == 'horizontal' else ydata

        if self._active_handle is None and not self.ignore_event_outside:
            # when the press event outside the span, we initially set the
            # visibility to False and extents to (v, v)
            # update will be called when setting the extents
            self._visible = False
            self.extents = v, v
            # We need to set the visibility back, so the span selector will be
            # drawn when necessary (span width > 0)
            self._visible = True
        else:
            self.set_visible(True)

        return False
