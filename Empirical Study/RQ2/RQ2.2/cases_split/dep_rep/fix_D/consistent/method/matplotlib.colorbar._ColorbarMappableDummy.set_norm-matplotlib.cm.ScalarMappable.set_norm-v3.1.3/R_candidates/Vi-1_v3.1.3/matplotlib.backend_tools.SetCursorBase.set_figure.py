    def set_figure(self, figure):
        if self._idDrag:
            self.canvas.mpl_disconnect(self._idDrag)
        ToolBase.set_figure(self, figure)
        if figure:
            self._idDrag = self.canvas.mpl_connect(
                'motion_notify_event', self._set_cursor_cbk)
