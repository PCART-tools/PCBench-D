    def release_pan(self, event):
        """Callback for mouse button release in pan/zoom mode."""
        if self._pan_info is None:
            return
        self.canvas.mpl_disconnect(self._pan_info.cid)
        self._id_drag = self.canvas.mpl_connect(
            'motion_notify_event', self.mouse_move)
        for ax in self._pan_info.axes:
            ax.end_pan()
        release = _api.deprecate_method_override(
            __class__.press, self, since="3.3", message="Calling an "
            "overridden release() at pan stop is deprecated since %(since)s "
            "and will be removed %(removal)s; override release_pan() instead.")
        if release is not None:
            release(event)
        self._draw()
        self._pan_info = None
        self.push_current()
