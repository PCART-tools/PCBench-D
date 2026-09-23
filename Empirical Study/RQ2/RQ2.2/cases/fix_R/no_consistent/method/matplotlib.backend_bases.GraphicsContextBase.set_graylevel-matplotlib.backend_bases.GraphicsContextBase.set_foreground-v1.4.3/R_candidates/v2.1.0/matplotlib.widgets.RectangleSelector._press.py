    def _press(self, event):
        """on button press event"""
        # make the drawed box/line visible get the click-coordinates,
        # button, ...
        if self.interactive and self.to_draw.get_visible():
            self._set_active_handle(event)
        else:
            self.active_handle = None

        if self.active_handle is None or not self.interactive:
            # Clear previous rectangle before drawing new rectangle.
            self.update()

        self.set_visible(self.visible)
