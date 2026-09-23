    def _print_svg(
            self, filename, fh, *, dpi=72, bbox_inches_restore=None, **kwargs):
        self.figure.set_dpi(72.0)
        width, height = self.figure.get_size_inches()
        w, h = width * 72, height * 72

        renderer = MixedModeRenderer(
            self.figure, width, height, dpi,
            RendererSVG(w, h, fh, filename, dpi),
            bbox_inches_restore=bbox_inches_restore)

        self.figure.draw(renderer)
        renderer.finalize()
