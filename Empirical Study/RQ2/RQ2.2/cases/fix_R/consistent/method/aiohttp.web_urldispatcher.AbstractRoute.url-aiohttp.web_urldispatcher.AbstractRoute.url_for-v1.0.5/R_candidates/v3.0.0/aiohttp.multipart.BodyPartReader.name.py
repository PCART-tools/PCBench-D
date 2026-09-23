    @reify
    def name(self):
        """Returns name specified in Content-Disposition header or None
        if missed or header is malformed.
        """
        _, params = parse_content_disposition(
            self.headers.get(CONTENT_DISPOSITION))
        return content_disposition_filename(params, 'name')
