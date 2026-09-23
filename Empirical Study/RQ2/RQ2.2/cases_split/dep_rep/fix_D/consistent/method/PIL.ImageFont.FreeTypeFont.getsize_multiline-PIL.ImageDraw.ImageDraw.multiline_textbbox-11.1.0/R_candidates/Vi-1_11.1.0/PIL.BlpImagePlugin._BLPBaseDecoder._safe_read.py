    def _safe_read(self, length: int) -> bytes:
        assert self.fd is not None
        return ImageFile._safe_read(self.fd, length)
