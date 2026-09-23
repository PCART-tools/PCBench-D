class FigureCanvasPdf(FigureCanvasBase):
    """
    The canvas the figure renders into.  Calls the draw and print fig
    methods, creates the renderers, etc...

    Attributes
    ----------
    figure : `matplotlib.figure.Figure`
        A high-level Figure instance

    """

    fixed_dpi = 72

    def draw(self):
        pass

    filetypes = {'pdf': 'Portable Document Format'}

    def get_default_filetype(self):
        return 'pdf'

    def print_pdf(self, filename, *,
                  dpi=72,  # dpi to use for images
                  bbox_inches_restore=None, metadata=None,
                  **kwargs):
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
