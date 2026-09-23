    def resize(self, w, h, forward=True):
        self._send_event(
            'resize',
            size=(w / self.canvas._dpi_ratio, h / self.canvas._dpi_ratio),
            forward=forward)
