    def set_content_disposition(self, disptype, quote_fields=True, **params):
        """Sets ``Content-Disposition`` header."""
        if self._headers is None:
            self._headers = CIMultiDict()

        self._headers[hdrs.CONTENT_DISPOSITION] = content_disposition_header(
            disptype, quote_fields=quote_fields, **params)
