    def set_content_disposition(self, disptype, quote_fields=True, **params):
        """Sets ``Content-Disposition`` header.

        :param str disptype: Disposition type: inline, attachment, form-data.
                            Should be valid extension token (see RFC 2183)
        :param dict params: Disposition params
        """
        if self._headers is None:
            self._headers = CIMultiDict()

        self._headers[hdrs.CONTENT_DISPOSITION] = content_disposition_header(
            disptype, quote_fields=quote_fields, **params)
