    @reify
    def filename(self):
        """Returns filename specified in Content-Disposition header or ``None``
        if missed or header is malformed."""
        _, params = parse_content_disposition(
            self.headers.get(CONTENT_DISPOSITION))
        return content_disposition_filename(params, 'filename')
