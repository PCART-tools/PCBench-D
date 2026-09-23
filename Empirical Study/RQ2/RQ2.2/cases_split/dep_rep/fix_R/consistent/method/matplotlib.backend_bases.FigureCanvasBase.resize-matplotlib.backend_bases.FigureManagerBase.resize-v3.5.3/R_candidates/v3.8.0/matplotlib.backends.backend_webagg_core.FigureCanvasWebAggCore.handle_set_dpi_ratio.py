    def handle_set_dpi_ratio(self, event):
        # This handler is for backwards-compatibility with older ipympl.
        self._handle_set_device_pixel_ratio(event.get('dpi_ratio', 1))
