class FigureCanvasPdf(FigureCanvasBase):
    # docstring inherited

    fixed_dpi = 72
    filetypes = {'pdf': 'Portable Document Format'}

    def get_default_filetype(self):
        return 'pdf'

    @_check_savefig_extra_args
    @_api.delete_parameter("3.4", "dpi")
    def print_pdf(self, filename, *,
                  dpi=None,  # dpi to use for images
                  bbox_inches_restore=None, metadata=None):

        if dpi is None:  # always use this branch after deprecation elapses.
            dpi = self.figure.get_dpi()
        self.figure.set_dpi(72)            # there are 72 pdf points to an inch
        width, height = self.figure.get_size_inches()
        if isinstance(filename, PdfPages):
            file = filename._file
        else:
            file = PdfFile(filename, metadata=metadata)
        try:
            file.newPage(width, height)
            renderer = MixedModeRenderer(
                self.figure, width, height, dpi,
                RendererPdf(file, dpi, height, width),
                bbox_inches_restore=bbox_inches_restore)
            self.figure.draw(renderer)
            renderer.finalize()
            if not isinstance(filename, PdfPages):
                file.finalize()
        finally:
            if isinstance(filename, PdfPages):  # finish off this page
                file.endStream()
            else:            # we opened the file above; now finish it off
                file.close()

    def draw(self):
        _no_output_draw(self.figure)
        return super().draw()
