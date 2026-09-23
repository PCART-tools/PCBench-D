    def release_pan(self, event):
        """Callback for mouse button release in pan/zoom mode."""

        if self._button_pressed is None:
            return
        self.canvas.mpl_disconnect(self._id_drag)
        self._id_drag = self.canvas.mpl_connect(
            'motion_notify_event', self.mouse_move)
        for a, ind in self._xypress:
            a.end_pan()
        if not self._xypress:
            return
        self._xypress = []
        self._button_pressed = None
        self.push_current()
        release = cbook._deprecate_method_override(
            __class__.press, self, since="3.3", message="Calling an "
            "overridden release() at pan stop is deprecated since %(since)s "
            "and will be removed %(removal)s; override release_pan() instead.")
        if release is not None:
            release(event)
        self._draw()
