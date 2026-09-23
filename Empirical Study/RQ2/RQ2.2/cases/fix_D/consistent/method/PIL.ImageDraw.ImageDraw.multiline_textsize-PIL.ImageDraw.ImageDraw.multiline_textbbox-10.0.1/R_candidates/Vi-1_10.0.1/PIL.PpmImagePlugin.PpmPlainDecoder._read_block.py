    def _read_block(self):
        return self.fd.read(ImageFile.SAFEBLOCK)
