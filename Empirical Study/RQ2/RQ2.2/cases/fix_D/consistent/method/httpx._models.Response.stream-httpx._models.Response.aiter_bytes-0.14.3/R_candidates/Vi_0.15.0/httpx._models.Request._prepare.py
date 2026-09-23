    def _prepare(self, default_headers: typing.Dict[str, str]) -> None:
        for key, value in default_headers.items():
            # Ignore Transfer-Encoding if the Content-Length has been set explicitly.
            if key.lower() == "transfer-encoding" and "content-length" in self.headers:
                continue
            self.headers.setdefault(key, value)

        auto_headers: typing.List[typing.Tuple[bytes, bytes]] = []

        has_host = "host" in self.headers
        has_content_length = (
            "content-length" in self.headers or "transfer-encoding" in self.headers
        )

        if not has_host and self.url.host:
            default_port = {"http": 80, "https": 443}.get(self.url.scheme)
            if self.url.port is None or self.url.port == default_port:
                host_header = self.url.host.encode("ascii")
            else:
                host_header = self.url.netloc.encode("ascii")
            auto_headers.append((b"host", host_header))
        if not has_content_length and self.method in ("POST", "PUT", "PATCH"):
            auto_headers.append((b"content-length", b"0"))

        self.headers = Headers(auto_headers + self.headers.raw)
