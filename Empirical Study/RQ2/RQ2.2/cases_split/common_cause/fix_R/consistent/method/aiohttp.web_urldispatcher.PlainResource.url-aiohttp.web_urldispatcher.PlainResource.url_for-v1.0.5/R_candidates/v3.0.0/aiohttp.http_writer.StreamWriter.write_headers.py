    def write_headers(self, status_line, headers, SEP=': ', END='\r\n'):
        """Write request/response status and headers."""
        # status + headers
        headers = status_line + ''.join(
            [k + SEP + v + END for k, v in headers.items()])
        headers = headers.encode('utf-8') + b'\r\n'
        self._write(headers)
