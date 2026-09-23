    def fixIFD(self) -> None:
        num_tags = self._read(8 if self._bigtiff else 2)

        for i in range(num_tags):
            tag, field_type, count = struct.unpack(
                self.tagFormat, self.f.read(12 if self._bigtiff else 8)
            )

            field_size = self.fieldSizes[field_type]
            total_size = field_size * count
            fmt_size = 8 if self._bigtiff else 4
            is_local = total_size <= fmt_size
            if not is_local:
                offset = self._read(fmt_size) + self.offsetOfNewPage
                self._rewriteLast(offset, fmt_size)

            if tag in self.Tags:
                cur_pos = self.f.tell()

                logger.debug(
                    "fixIFD: %s (%d) - type: %s (%d) - type size: %d - count: %d",
                    TiffTags.lookup(tag).name,
                    tag,
                    TYPES.get(field_type, "unknown"),
                    field_type,
                    field_size,
                    count,
                )

                if is_local:
                    self._fixOffsets(count, field_size)
                    self.f.seek(cur_pos + fmt_size)
                else:
                    self.f.seek(offset)
                    self._fixOffsets(count, field_size)
                    self.f.seek(cur_pos)

            elif is_local:
                # skip the locally stored value that is not an offset
                self.f.seek(fmt_size, os.SEEK_CUR)
