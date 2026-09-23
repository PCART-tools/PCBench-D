    def _read_block(self) -> bytes:
        assert self.fd is not None

        return self.fd.read(ImageFile.SAFEBLOCK)
