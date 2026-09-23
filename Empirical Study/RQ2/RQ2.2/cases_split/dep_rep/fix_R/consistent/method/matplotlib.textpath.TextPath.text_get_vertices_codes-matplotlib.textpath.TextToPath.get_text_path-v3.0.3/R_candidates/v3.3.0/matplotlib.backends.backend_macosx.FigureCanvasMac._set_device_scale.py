    def _set_device_scale(self, value):
        if self._dpi_ratio != value:
            # Need the new value in place before setting figure.dpi, which
            # will trigger a resize
            self._dpi_ratio, old_value = value, self._dpi_ratio
            self.figure.dpi = self.figure.dpi / old_value * self._dpi_ratio
