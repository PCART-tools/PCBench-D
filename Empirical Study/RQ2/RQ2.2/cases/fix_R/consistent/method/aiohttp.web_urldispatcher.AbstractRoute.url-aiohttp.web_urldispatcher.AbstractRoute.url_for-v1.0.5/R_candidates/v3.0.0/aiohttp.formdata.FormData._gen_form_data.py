    def _gen_form_data(self):
        """Encode a list of fields using the multipart/form-data MIME format"""
        for dispparams, headers, value in self._fields:
            try:
                if hdrs.CONTENT_TYPE in headers:
                    part = payload.get_payload(
                        value, content_type=headers[hdrs.CONTENT_TYPE],
                        headers=headers, encoding=self._charset)
                else:
                    part = payload.get_payload(
                        value, headers=headers, encoding=self._charset)
            except Exception as exc:
                raise TypeError(
                    'Can not serialize value type: %r\n '
                    'headers: %r\n value: %r' % (
                        type(value), headers, value)) from exc

            if dispparams:
                part.set_content_disposition(
                    'form-data', quote_fields=self._quote_fields, **dispparams
                )
                # FIXME cgi.FieldStorage doesn't likes body parts with
                # Content-Length which were sent via chunked transfer encoding
                part.headers.popall(hdrs.CONTENT_LENGTH, None)

            self._writer.append_payload(part)

        return self._writer
