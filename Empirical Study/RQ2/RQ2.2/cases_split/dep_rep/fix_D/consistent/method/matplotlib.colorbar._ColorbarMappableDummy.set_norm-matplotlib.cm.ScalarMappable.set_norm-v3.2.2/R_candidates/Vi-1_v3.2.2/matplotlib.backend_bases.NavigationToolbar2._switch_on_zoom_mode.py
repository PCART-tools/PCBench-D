    def _switch_on_zoom_mode(self, event):
        self._zoom_mode = event.key
        self.mouse_move(event)
