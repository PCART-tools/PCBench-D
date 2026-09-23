    def release_pan(self, event):
        """Callback for mouse button release in pan/zoom mode."""

        if self._button_pressed is None:
            return
        self.canvas.mpl_disconnect(self._idDrag)
        self._idDrag = self.canvas.mpl_connect(
            'motion_notify_event', self.mouse_move)
        for a, ind in self._xypress:
            a.end_pan()
        if not self._xypress:
            return
        self._xypress = []
        self._button_pressed = None
        self.push_current()
        self.release(event)
        self.draw()
