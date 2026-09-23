    def _cancel_action(self):
        for zoom_id in self._ids_zoom:
            self.figure.canvas.mpl_disconnect(zoom_id)
        self.toolmanager.trigger_tool('rubberband', self)
        self.figure.canvas.draw_idle()
        self._xypress = None
        self._button_pressed = None
        self._ids_zoom = []
        return
