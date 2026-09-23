    def resize(self, w, h, forward=True):
        self._send_event(
            'resize',
            size=(w / self.canvas.device_pixel_ratio,
                  h / self.canvas.device_pixel_ratio),
            forward=forward)
