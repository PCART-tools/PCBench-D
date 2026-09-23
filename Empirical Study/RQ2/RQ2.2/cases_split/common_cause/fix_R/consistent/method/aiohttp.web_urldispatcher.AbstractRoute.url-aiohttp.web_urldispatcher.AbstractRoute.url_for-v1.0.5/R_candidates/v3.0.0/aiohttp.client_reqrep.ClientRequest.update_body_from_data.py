    def update_body_from_data(self, body):
        if not body:
            return

        # FormData
        if isinstance(body, FormData):
            body = body()

        try:
            body = payload.PAYLOAD_REGISTRY.get(body, disposition=None)
        except payload.LookupError:
            body = FormData(body)()

        self.body = body

        # enable chunked encoding if needed
        if not self.chunked:
            if hdrs.CONTENT_LENGTH not in self.headers:
                size = body.size
                if size is None:
                    self.chunked = True
                else:
                    if hdrs.CONTENT_LENGTH not in self.headers:
                        self.headers[hdrs.CONTENT_LENGTH] = str(size)

        # set content-type
        if (hdrs.CONTENT_TYPE not in self.headers and
                hdrs.CONTENT_TYPE not in self.skip_auto_headers):
            self.headers[hdrs.CONTENT_TYPE] = body.content_type

        # copy payload headers
        if body.headers:
            for (key, value) in body.headers.items():
                if key not in self.headers:
                    self.headers[key] = value
