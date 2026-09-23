    def set_figure(self, figure):
        if self._id_drag:
            self.canvas.mpl_disconnect(self._id_drag)
        ToolBase.set_figure(self, figure)
        if figure:
            self._id_drag = self.canvas.mpl_connect(
                'motion_notify_event', self._set_cursor_cbk)
