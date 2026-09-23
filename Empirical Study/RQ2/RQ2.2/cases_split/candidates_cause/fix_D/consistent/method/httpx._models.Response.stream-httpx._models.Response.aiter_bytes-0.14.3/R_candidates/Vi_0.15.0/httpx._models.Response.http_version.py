    @property
    def http_version(self) -> str:
        return self.ext.get("http_version", "HTTP/1.1")
