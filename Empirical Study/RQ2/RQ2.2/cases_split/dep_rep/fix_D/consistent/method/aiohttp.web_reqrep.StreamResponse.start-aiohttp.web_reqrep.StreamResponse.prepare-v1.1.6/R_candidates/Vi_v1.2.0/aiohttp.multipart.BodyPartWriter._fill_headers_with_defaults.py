    def _fill_headers_with_defaults(self):
        if CONTENT_TYPE not in self.headers:
            content_type = self._guess_content_type(self.obj)
            if content_type is not None:
                self.headers[CONTENT_TYPE] = content_type

        if CONTENT_LENGTH not in self.headers:
            content_length = self._guess_content_length(self.obj)
            if content_length is not None:
                self.headers[CONTENT_LENGTH] = str(content_length)

        if CONTENT_DISPOSITION not in self.headers:
            filename = self._guess_filename(self.obj)
            if filename is not None:
                self.set_content_disposition('attachment', filename=filename)
