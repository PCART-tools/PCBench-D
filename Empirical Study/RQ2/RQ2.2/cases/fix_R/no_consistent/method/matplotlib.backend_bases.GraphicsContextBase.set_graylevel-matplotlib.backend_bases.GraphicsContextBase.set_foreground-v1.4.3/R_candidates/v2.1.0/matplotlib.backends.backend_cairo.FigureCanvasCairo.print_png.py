    def print_png(self, fobj, *args, **kwargs):
        width, height = self.get_width_height()

        renderer = RendererCairo(self.figure.dpi)
        renderer.set_width_height(width, height)
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        renderer.set_ctx_from_surface(surface)

        self.figure.draw(renderer)
        surface.write_to_png(fobj)
