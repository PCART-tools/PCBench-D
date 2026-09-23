    def seek(self, offset, whence=io.SEEK_SET):
        self.char = None
        self.fp.seek(offset, whence)
