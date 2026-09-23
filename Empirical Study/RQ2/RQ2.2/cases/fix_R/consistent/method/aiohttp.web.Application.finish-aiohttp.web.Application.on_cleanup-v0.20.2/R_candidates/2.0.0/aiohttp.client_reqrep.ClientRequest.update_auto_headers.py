    def update_auto_headers(self, skip_auto_headers):
        self.skip_auto_headers = skip_auto_headers
        used_headers = set(self.headers) | skip_auto_headers

        for hdr, val in self.DEFAULT_HEADERS.items():
            if hdr not in used_headers:
                self.headers.add(hdr, val)

        # add host
        if hdrs.HOST not in used_headers:
            netloc = self.url.raw_host
            if not self.url.is_default_port():
                netloc += ':' + str(self.url.port)
            self.headers[hdrs.HOST] = netloc

        if hdrs.USER_AGENT not in used_headers:
            self.headers[hdrs.USER_AGENT] = SERVER_SOFTWARE
