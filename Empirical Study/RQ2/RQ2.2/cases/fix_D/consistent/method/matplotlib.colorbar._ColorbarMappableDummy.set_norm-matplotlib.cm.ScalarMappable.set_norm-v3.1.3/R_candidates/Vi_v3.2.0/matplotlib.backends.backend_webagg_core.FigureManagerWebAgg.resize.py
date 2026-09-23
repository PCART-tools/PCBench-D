    def resize(self, w, h):
        self._send_event(
            'resize',
            size=(w / self.canvas._dpi_ratio, h / self.canvas._dpi_ratio))
