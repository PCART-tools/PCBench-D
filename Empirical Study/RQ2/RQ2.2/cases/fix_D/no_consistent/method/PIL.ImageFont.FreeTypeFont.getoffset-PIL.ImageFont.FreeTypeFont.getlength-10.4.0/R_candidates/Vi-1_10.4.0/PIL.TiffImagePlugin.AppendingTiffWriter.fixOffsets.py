    def fixOffsets(
        self, count: int, isShort: bool = False, isLong: bool = False
    ) -> None:
        if not isShort and not isLong:
            msg = "offset is neither short nor long"
            raise RuntimeError(msg)

        for i in range(count):
            offset = self.readShort() if isShort else self.readLong()
            offset += self.offsetOfNewPage
            if isShort and offset >= 65536:
                # offset is now too large - we must convert shorts to longs
                if count != 1:
                    msg = "not implemented"
                    raise RuntimeError(msg)  # XXX TODO

                # simple case - the offset is just one and therefore it is
                # local (not referenced with another offset)
                self.rewriteLastShortToLong(offset)
                self.f.seek(-10, os.SEEK_CUR)
                self.writeShort(TiffTags.LONG)  # rewrite the type to LONG
                self.f.seek(8, os.SEEK_CUR)
            elif isShort:
                self.rewriteLastShort(offset)
            else:
                self.rewriteLastLong(offset)
