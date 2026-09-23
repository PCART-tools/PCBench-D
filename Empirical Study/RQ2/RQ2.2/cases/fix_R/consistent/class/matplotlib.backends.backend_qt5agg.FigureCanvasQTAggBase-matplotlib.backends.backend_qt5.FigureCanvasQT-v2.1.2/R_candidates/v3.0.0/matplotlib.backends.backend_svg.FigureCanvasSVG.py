class FigureCanvasSVG(FigureCanvasBase):
    filetypes = {'svg': 'Scalable Vector Graphics',
                 'svgz': 'Scalable Vector Graphics'}

    fixed_dpi = 72

    def print_svg(self, filename, *args, **kwargs):
        with cbook.open_file_cm(filename, "w", encoding="utf-8") as fh:

            filename = getattr(fh, 'name', '')
            if not isinstance(filename, str):
                filename = ''

            if cbook.file_requires_unicode(fh):
                detach = False
            else:
                fh = io.TextIOWrapper(fh, 'utf-8')
                detach = True

            result = self._print_svg(filename, fh, **kwargs)

            # Detach underlying stream from wrapper so that it remains open in
            # the caller.
            if detach:
                fh.detach()

        return result

    def print_svgz(self, filename, *args, **kwargs):
        with cbook.open_file_cm(filename, "wb") as fh, \
                gzip.GzipFile(mode='w', fileobj=fh) as gzipwriter:
            return self.print_svg(gzipwriter)

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

    def get_default_filetype(self):
        return 'svg'
