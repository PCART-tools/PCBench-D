    def _print_svg(self, filename, svgwriter, **kwargs):
        image_dpi = kwargs.pop("dpi", 72)
        self.figure.set_dpi(72.0)
        width, height = self.figure.get_size_inches()
        w, h = width*72, height*72

        _bbox_inches_restore = kwargs.pop("bbox_inches_restore", None)
        renderer = MixedModeRenderer(
            self.figure,
            width, height, image_dpi, RendererSVG(w, h, svgwriter, filename, image_dpi),
            bbox_inches_restore=_bbox_inches_restore)

        self.figure.draw(renderer)
        renderer.finalize()
