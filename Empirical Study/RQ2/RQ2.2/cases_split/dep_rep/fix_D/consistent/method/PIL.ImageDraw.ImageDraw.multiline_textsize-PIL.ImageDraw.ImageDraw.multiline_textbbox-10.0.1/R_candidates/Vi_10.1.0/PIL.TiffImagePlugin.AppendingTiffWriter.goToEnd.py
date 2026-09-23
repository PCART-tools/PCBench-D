    def goToEnd(self):
        self.f.seek(0, os.SEEK_END)
        pos = self.f.tell()

        # pad to 16 byte boundary
        pad_bytes = 16 - pos % 16
        if 0 < pad_bytes < 16:
            self.f.write(bytes(pad_bytes))
        self.offsetOfNewPage = self.f.tell()
