    @reify
    def content_disposition(self):
        raw = self._headers.get(hdrs.CONTENT_DISPOSITION)
        if raw is None:
            return None
        disposition_type, params = multipart.parse_content_disposition(raw)
        params = MappingProxyType(params)
        filename = multipart.content_disposition_filename(params)
        return ContentDisposition(disposition_type, params, filename)
