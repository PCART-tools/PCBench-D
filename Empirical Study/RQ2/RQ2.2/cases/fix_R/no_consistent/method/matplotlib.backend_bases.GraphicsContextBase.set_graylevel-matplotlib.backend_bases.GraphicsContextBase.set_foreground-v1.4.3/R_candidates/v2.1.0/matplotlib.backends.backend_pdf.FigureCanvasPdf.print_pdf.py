    def print_pdf(self, filename, **kwargs):
        image_dpi = kwargs.get('dpi', 72)  # dpi to use for images
        self.figure.set_dpi(72)            # there are 72 pdf points to an inch
        width, height = self.figure.get_size_inches()
        if isinstance(filename, PdfPages):
            file = filename._file
        else:
            file = PdfFile(filename, metadata=kwargs.pop("metadata", None))
        try:
            file.newPage(width, height)
            _bbox_inches_restore = kwargs.pop("bbox_inches_restore", None)
            renderer = MixedModeRenderer(
                self.figure, width, height, image_dpi,
                RendererPdf(file, image_dpi, height, width),
                bbox_inches_restore=_bbox_inches_restore)
            self.figure.draw(renderer)
            renderer.finalize()
            file.finalize()
        finally:
            if isinstance(filename, PdfPages):  # finish off this page
                file.endStream()
            else:            # we opened the file above; now finish it off
                file.close()
