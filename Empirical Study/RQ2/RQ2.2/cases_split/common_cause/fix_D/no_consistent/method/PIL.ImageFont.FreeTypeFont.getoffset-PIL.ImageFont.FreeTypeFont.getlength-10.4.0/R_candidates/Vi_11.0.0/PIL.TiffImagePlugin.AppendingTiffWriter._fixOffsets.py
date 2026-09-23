    def _fixOffsets(self, count: int, field_size: int) -> None:
        for i in range(count):
            offset = self._read(field_size)
            offset += self.offsetOfNewPage
            if field_size == 2 and offset >= 65536:
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
            else:
                self._rewriteLast(offset, field_size)
