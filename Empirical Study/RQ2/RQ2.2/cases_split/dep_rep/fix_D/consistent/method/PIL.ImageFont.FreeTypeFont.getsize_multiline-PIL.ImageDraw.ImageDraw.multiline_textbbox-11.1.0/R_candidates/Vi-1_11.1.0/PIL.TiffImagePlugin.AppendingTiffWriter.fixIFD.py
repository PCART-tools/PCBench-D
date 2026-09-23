    def fixIFD(self) -> None:
        num_tags = self.readShort()

        for i in range(num_tags):
            tag, field_type, count = struct.unpack(self.tagFormat, self.f.read(8))

            field_size = self.fieldSizes[field_type]
            total_size = field_size * count
            is_local = total_size <= 4
            if not is_local:
                offset = self.readLong() + self.offsetOfNewPage
                self.rewriteLastLong(offset)

            if tag in self.Tags:
                cur_pos = self.f.tell()

                if is_local:
                    self._fixOffsets(count, field_size)
                    self.f.seek(cur_pos + 4)
                else:
                    self.f.seek(offset)
                    self._fixOffsets(count, field_size)
                    self.f.seek(cur_pos)

            elif is_local:
                # skip the locally stored value that is not an offset
                self.f.seek(4, os.SEEK_CUR)
