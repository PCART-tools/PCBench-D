    def finalize(self) -> None:
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

        if self._bigtiff:
            self.f.seek(4, os.SEEK_CUR)
        ifd_offset = self._read(8 if self._bigtiff else 4)
        ifd_offset += self.offsetOfNewPage
        assert self.whereToWriteNewIFDOffset is not None
        self.f.seek(self.whereToWriteNewIFDOffset)
        self._write(ifd_offset, 8 if self._bigtiff else 4)
        self.f.seek(ifd_offset)
        self.fixIFD()
