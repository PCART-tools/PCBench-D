    def add_headers(self, *headers):
        """Adds headers to a HTTP message."""
        for name, value in headers:
            self.add_header(name, value)
