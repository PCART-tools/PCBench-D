    def _get_printed_image_surface(self):
        self._renderer.dpi = self.figure.dpi
        width, height = self.get_width_height()
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        self._renderer.set_context(cairo.Context(surface))
        self.figure.draw(self._renderer)
        return surface
