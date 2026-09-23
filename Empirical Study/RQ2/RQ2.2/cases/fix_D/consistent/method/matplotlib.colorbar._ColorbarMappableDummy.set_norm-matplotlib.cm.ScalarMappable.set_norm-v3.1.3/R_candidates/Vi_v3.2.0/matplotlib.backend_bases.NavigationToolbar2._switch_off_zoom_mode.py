    def _switch_off_zoom_mode(self, event):
        self._zoom_mode = None
        self.mouse_move(event)
