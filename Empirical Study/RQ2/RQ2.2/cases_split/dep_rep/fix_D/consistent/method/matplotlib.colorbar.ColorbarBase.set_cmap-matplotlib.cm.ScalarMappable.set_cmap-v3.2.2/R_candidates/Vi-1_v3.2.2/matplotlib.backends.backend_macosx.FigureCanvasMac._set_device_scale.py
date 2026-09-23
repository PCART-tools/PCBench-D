    def _set_device_scale(self, value):
        if self._device_scale != value:
            self.figure.dpi = self.figure.dpi / self._device_scale * value
            self._device_scale = value
