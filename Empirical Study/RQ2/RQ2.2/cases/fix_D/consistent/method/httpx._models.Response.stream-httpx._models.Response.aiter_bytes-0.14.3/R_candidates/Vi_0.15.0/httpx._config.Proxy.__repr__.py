    def __repr__(self) -> str:
        return (
            f"Proxy(url={str(self.url)!r}, "
            f"headers={dict(self.headers)!r}, "
            f"mode={self.mode!r})"
        )
