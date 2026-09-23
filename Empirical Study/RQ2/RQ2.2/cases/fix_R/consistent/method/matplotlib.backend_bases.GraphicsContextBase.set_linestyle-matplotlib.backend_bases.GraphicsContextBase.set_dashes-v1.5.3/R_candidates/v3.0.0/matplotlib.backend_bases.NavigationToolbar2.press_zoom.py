    def press_zoom(self, event):
        """Callback for mouse button press in zoom to rect mode."""
        # If we're already in the middle of a zoom, pressing another
        # button works to "cancel"
        if self._ids_zoom != []:
            for zoom_id in self._ids_zoom:
                self.canvas.mpl_disconnect(zoom_id)
            self.release(event)
            self.draw()
            self._xypress = None
            self._button_pressed = None
            self._ids_zoom = []
            return

        if event.button == 1:
            self._button_pressed = 1
        elif event.button == 3:
            self._button_pressed = 3
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
                    a.get_navigate() and a.can_zoom()):
                self._xypress.append((x, y, a, i, a._get_view()))

        id1 = self.canvas.mpl_connect('motion_notify_event', self.drag_zoom)
        id2 = self.canvas.mpl_connect('key_press_event',
                                      self._switch_on_zoom_mode)
        id3 = self.canvas.mpl_connect('key_release_event',
                                      self._switch_off_zoom_mode)

        self._ids_zoom = id1, id2, id3
        self._zoom_mode = event.key

        self.press(event)
