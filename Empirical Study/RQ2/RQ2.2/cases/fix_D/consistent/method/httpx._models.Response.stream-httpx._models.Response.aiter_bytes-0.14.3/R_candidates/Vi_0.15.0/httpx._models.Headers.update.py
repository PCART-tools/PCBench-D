    def update(self, headers: HeaderTypes = None) -> None:  # type: ignore
        headers = Headers(headers)
        for header in headers:
            self[header] = headers[header]
