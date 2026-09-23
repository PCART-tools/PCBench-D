    def _press(self, event):
        """Button press event handler."""
        # make the drawn box/line visible get the click-coordinates,
        # button, ...
        if self.interactive and self.to_draw.get_visible():
            self._set_active_handle(event)
        else:
            self.active_handle = None

        if self.active_handle is None or not self.interactive:
            # Clear previous rectangle before drawing new rectangle.
            self.update()

        if not self.interactive:
            x = event.xdata
            y = event.ydata
            self.extents = x, x, y, y

        self.set_visible(self.visible)
