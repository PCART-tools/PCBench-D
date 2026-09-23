    def _press(self, event):
        """Button press event handler."""
        # make the drawn box/line visible get the click-coordinates,
        # button, ...
        if self._interactive and self._selection_artist.get_visible():
            self._set_active_handle(event)
        else:
            self._active_handle = None

        if ((self._active_handle is None or not self._interactive) and
                self._allow_creation):
            # Clear previous rectangle before drawing new rectangle.
            self.update()

        if (self._active_handle is None and not self.ignore_event_outside and
                self._allow_creation):
            x = event.xdata
            y = event.ydata
            self._visible = False
            self.extents = x, x, y, y
            self._visible = True
        else:
            self.set_visible(True)

        self._extents_on_press = self.extents
        self._rotation_on_press = self._rotation
        self._set_aspect_ratio_correction()

        return False
