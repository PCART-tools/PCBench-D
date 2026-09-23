    def press_pan(self, event):
        """Callback for mouse button press in pan/zoom mode."""
        if event.button in [1, 3]:
            self._button_pressed = event.button
        else:
            self._button_pressed = None
            return
        if self._nav_stack() is None:
            # set the home button to this view
            self.push_current()
        x, y = event.x, event.y
        self._xypress = []
        for i, a in enumerate(self.canvas.figure.get_axes()):
            if (x is not None and y is not None and a.in_axes(event) and
                    a.get_navigate() and a.can_pan()):
                a.start_pan(x, y, event.button)
                self._xypress.append((a, i))
                self.canvas.mpl_disconnect(self._id_drag)
                self._id_drag = self.canvas.mpl_connect(
                    'motion_notify_event', self.drag_pan)
        press = cbook._deprecate_method_override(
            __class__.press, self, since="3.3", message="Calling an "
            "overridden press() at pan start is deprecated since %(since)s "
            "and will be removed %(removal)s; override press_pan() instead.")
        if press is not None:
            press(event)
