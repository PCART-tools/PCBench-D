    def _fixOffsets(self, count: int, field_size: int) -> None:
        for i in range(count):
            offset = self._read(field_size)
            offset += self.offsetOfNewPage

            new_field_size = 0
            if self._bigtiff and field_size in (2, 4) and offset >= 2**32:
                # offset is now too large - we must convert long to long8
                new_field_size = 8
            elif field_size == 2 and offset >= 2**16:
                # offset is now too large - we must convert short to long
                new_field_size = 4
            if new_field_size:
                if count != 1:
                    msg = "not implemented"
                    raise RuntimeError(msg)  # XXX TODO

                # simple case - the offset is just one and therefore it is
                # local (not referenced with another offset)
                self._rewriteLast(offset, field_size, new_field_size)
                # Move back past the new offset, past 'count', and before 'field_type'
                rewind = -new_field_size - 4 - 2
                self.f.seek(rewind, os.SEEK_CUR)
                self.writeShort(new_field_size)  # rewrite the type
                self.f.seek(2 - rewind, os.SEEK_CUR)
            else:
                self._rewriteLast(offset, field_size)
