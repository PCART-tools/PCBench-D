    def setup(self):
        # Reset everything.
        self.f.seek(self.beginning, os.SEEK_SET)

        self.whereToWriteNewIFDOffset = None
        self.offsetOfNewPage = 0

        self.IIMM = iimm = self.f.read(4)
        if not iimm:
            # empty file - first page
            self.isFirst = True
            return

        self.isFirst = False
        if iimm == b"II\x2a\x00":
            self.setEndian("<")
        elif iimm == b"MM\x00\x2a":
            self.setEndian(">")
        else:
            msg = "Invalid TIFF file header"
            raise RuntimeError(msg)

        self.skipIFDs()
        self.goToEnd()
