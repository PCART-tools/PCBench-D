    def resize(self, width, height):
        width = int(width / self.canvas.device_pixel_ratio)
        height = int(height / self.canvas.device_pixel_ratio)
        if self.toolbar:
            toolbar_size = self.toolbar.size_request()
            height += toolbar_size.height
        canvas_size = self.canvas.get_allocation()
        if self._gtk_ver >= 4 or canvas_size.width == canvas_size.height == 1:
            # A canvas size of (1, 1) cannot exist in most cases, because
            # window decorations would prevent such a small window. This call
            # must be before the window has been mapped and widgets have been
            # sized, so just change the window's starting size.
            self.window.set_default_size(width, height)
        else:
            self.window.resize(width, height)
