    def setup(self) -> None:
        # Reset everything.
        self.f.seek(self.beginning, os.SEEK_SET)

        self.whereToWriteNewIFDOffset: int | None = None
        self.offsetOfNewPage = 0

        self.IIMM = iimm = self.f.read(4)
        self._bigtiff = b"\x2b" in iimm
        if not iimm:
            # empty file - first page
            self.isFirst = True
            return

        self.isFirst = False
        if iimm not in PREFIXES:
            msg = "Invalid TIFF file header"
            raise RuntimeError(msg)

        self.setEndian("<" if iimm.startswith(II) else ">")

        if self._bigtiff:
            self.f.seek(4, os.SEEK_CUR)
        self.skipIFDs()
        self.goToEnd()
