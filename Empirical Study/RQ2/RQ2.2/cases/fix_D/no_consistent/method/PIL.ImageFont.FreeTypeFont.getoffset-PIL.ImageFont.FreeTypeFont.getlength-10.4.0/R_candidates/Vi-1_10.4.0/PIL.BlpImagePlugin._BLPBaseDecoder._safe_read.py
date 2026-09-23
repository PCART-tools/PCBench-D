    def _safe_read(self, length: int) -> bytes:
        return ImageFile._safe_read(self.fd, length)
