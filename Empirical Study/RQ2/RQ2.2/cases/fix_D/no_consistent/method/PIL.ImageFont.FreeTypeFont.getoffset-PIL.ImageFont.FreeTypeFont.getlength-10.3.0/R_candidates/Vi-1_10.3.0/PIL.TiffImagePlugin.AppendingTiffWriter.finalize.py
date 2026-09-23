    def finalize(self):
        if self.isFirst:
            return

        # fix offsets
        self.f.seek(self.offsetOfNewPage)

        iimm = self.f.read(4)
        if not iimm:
            # Make it easy to finish a frame without committing to a new one.
            return

        if iimm != self.IIMM:
            msg = "IIMM of new page doesn't match IIMM of first page"
            raise RuntimeError(msg)

        ifd_offset = self.readLong()
        ifd_offset += self.offsetOfNewPage
        self.f.seek(self.whereToWriteNewIFDOffset)
        self.writeLong(ifd_offset)
        self.f.seek(ifd_offset)
        self.fixIFD()
