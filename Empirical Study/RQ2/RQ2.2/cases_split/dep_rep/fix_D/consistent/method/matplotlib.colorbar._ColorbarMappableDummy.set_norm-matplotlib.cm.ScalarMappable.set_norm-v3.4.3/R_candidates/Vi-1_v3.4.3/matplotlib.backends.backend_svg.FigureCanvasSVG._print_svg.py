    @_check_savefig_extra_args
    @_api.delete_parameter("3.4", "dpi")
    def _print_svg(self, filename, fh, *, dpi=None, bbox_inches_restore=None,
                   metadata=None):
        if dpi is None:  # always use this branch after deprecation elapses.
            dpi = self.figure.get_dpi()
        self.figure.set_dpi(72)
        width, height = self.figure.get_size_inches()
        w, h = width * 72, height * 72

        renderer = MixedModeRenderer(
            self.figure, width, height, dpi,
            RendererSVG(w, h, fh, filename, dpi, metadata=metadata),
            bbox_inches_restore=bbox_inches_restore)

        self.figure.draw(renderer)
        renderer.finalize()
