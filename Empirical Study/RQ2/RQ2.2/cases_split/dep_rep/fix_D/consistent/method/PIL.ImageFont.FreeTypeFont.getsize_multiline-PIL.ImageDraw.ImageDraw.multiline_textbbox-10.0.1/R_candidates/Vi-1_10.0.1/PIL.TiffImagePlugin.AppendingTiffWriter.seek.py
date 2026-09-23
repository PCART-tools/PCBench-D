    def seek(self, offset, whence=io.SEEK_SET):
        if whence == os.SEEK_SET:
            offset += self.offsetOfNewPage

        self.f.seek(offset, whence)
        return self.tell()
