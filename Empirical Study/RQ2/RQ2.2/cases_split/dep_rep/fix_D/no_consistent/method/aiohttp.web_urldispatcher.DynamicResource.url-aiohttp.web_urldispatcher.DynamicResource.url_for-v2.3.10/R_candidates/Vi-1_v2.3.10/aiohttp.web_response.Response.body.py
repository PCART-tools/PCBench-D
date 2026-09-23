    @body.setter
    def body(self, body,
             CONTENT_TYPE=hdrs.CONTENT_TYPE,
             CONTENT_LENGTH=hdrs.CONTENT_LENGTH):
        if body is None:
            self._body = None
            self._body_payload = False
        elif isinstance(body, (bytes, bytearray)):
            self._body = body
            self._body_payload = False
        else:
            try:
                self._body = body = payload.PAYLOAD_REGISTRY.get(body)
            except payload.LookupError:
                raise ValueError('Unsupported body type %r' % type(body))

            self._body_payload = True

            headers = self._headers

            # set content-length header if needed
            if not self._chunked and CONTENT_LENGTH not in headers:
                size = body.size
                if size is not None:
                    headers[CONTENT_LENGTH] = str(size)

            # set content-type
            if CONTENT_TYPE not in headers:
                headers[CONTENT_TYPE] = body.content_type

            # copy payload headers
            if body.headers:
                for (key, value) in body.headers.items():
                    if key not in headers:
                        headers[key] = value

        self._compressed_body = None
