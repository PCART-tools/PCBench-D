    def update_body_from_data(self, data, skip_auto_headers):
        if not data:
            return

        if isinstance(data, str):
            data = data.encode(self.encoding)

        if isinstance(data, (bytes, bytearray)):
            self.body = data
            if (hdrs.CONTENT_TYPE not in self.headers and
                    hdrs.CONTENT_TYPE not in skip_auto_headers):
                self.headers[hdrs.CONTENT_TYPE] = 'application/octet-stream'
            if hdrs.CONTENT_LENGTH not in self.headers and not self.chunked:
                self.headers[hdrs.CONTENT_LENGTH] = str(len(self.body))

        elif isinstance(data, (asyncio.StreamReader, streams.StreamReader,
                               streams.DataQueue)):
            self.body = data

        elif asyncio.iscoroutine(data):
            self.body = data
            if (hdrs.CONTENT_LENGTH not in self.headers and
                    self.chunked is None):
                self.chunked = True

        elif isinstance(data, io.IOBase):
            assert not isinstance(data, io.StringIO), \
                'attempt to send text data instead of binary'
            self.body = data
            if not self.chunked and isinstance(data, io.BytesIO):
                # Not chunking if content-length can be determined
                size = len(data.getbuffer())
                self.headers[hdrs.CONTENT_LENGTH] = str(size)
                self.chunked = False
            elif (not self.chunked and
                  isinstance(data, (io.BufferedReader, io.BufferedRandom))):
                # Not chunking if content-length can be determined
                try:
                    size = os.fstat(data.fileno()).st_size - data.tell()
                    self.headers[hdrs.CONTENT_LENGTH] = str(size)
                    self.chunked = False
                except OSError:
                    # data.fileno() is not supported, e.g.
                    # io.BufferedReader(io.BytesIO(b'data'))
                    self.chunked = True
            else:
                self.chunked = True

            if hasattr(data, 'mode'):
                if data.mode == 'r':
                    raise ValueError('file {!r} should be open in binary mode'
                                     ''.format(data))
            if (hdrs.CONTENT_TYPE not in self.headers and
                hdrs.CONTENT_TYPE not in skip_auto_headers and
                    hasattr(data, 'name')):
                mime = mimetypes.guess_type(data.name)[0]
                mime = 'application/octet-stream' if mime is None else mime
                self.headers[hdrs.CONTENT_TYPE] = mime

        elif isinstance(data, MultipartWriter):
            self.body = data.serialize()
            self.headers.update(data.headers)
            self.chunked = self.chunked or 8192

        else:
            if not isinstance(data, helpers.FormData):
                data = helpers.FormData(data)

            self.body = data(self.encoding)

            if (hdrs.CONTENT_TYPE not in self.headers and
                    hdrs.CONTENT_TYPE not in skip_auto_headers):
                self.headers[hdrs.CONTENT_TYPE] = data.content_type

            if data.is_multipart:
                self.chunked = self.chunked or 8192
            else:
                if (hdrs.CONTENT_LENGTH not in self.headers and
                        not self.chunked):
                    self.headers[hdrs.CONTENT_LENGTH] = str(len(self.body))
