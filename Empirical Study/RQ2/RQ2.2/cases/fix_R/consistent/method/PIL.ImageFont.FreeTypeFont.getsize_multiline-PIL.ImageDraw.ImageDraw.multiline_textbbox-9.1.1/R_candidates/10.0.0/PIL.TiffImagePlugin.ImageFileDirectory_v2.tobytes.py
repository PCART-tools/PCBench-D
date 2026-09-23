    def tobytes(self, offset=0):
        # FIXME What about tagdata?
        result = self._pack("H", len(self._tags_v2))

        entries = []
        offset = offset + len(result) + len(self._tags_v2) * 12 + 4
        stripoffsets = None

        # pass 1: convert tags to binary format
        # always write tags in ascending order
        for tag, value in sorted(self._tags_v2.items()):
            if tag == STRIPOFFSETS:
                stripoffsets = len(entries)
            typ = self.tagtype.get(tag)
            logger.debug(f"Tag {tag}, Type: {typ}, Value: {repr(value)}")
            is_ifd = typ == TiffTags.LONG and isinstance(value, dict)
            if is_ifd:
                if self._endian == "<":
                    ifh = b"II\x2A\x00\x08\x00\x00\x00"
                else:
                    ifh = b"MM\x00\x2A\x00\x00\x00\x08"
                ifd = ImageFileDirectory_v2(ifh, group=tag)
                values = self._tags_v2[tag]
                for ifd_tag, ifd_value in values.items():
                    ifd[ifd_tag] = ifd_value
                data = ifd.tobytes(offset)
            else:
                values = value if isinstance(value, tuple) else (value,)
                data = self._write_dispatch[typ](self, *values)

            tagname = TiffTags.lookup(tag, self.group).name
            typname = "ifd" if is_ifd else TYPES.get(typ, "unknown")
            msg = f"save: {tagname} ({tag}) - type: {typname} ({typ})"
            msg += " - value: " + (
                "<table: %d bytes>" % len(data) if len(data) >= 16 else str(values)
            )
            logger.debug(msg)

            # count is sum of lengths for string and arbitrary data
            if is_ifd:
                count = 1
            elif typ in [TiffTags.BYTE, TiffTags.ASCII, TiffTags.UNDEFINED]:
                count = len(data)
            else:
                count = len(values)
            # figure out if data fits into the entry
            if len(data) <= 4:
                entries.append((tag, typ, count, data.ljust(4, b"\0"), b""))
            else:
                entries.append((tag, typ, count, self._pack("L", offset), data))
                offset += (len(data) + 1) // 2 * 2  # pad to word

        # update strip offset data to point beyond auxiliary data
        if stripoffsets is not None:
            tag, typ, count, value, data = entries[stripoffsets]
            if data:
                msg = "multistrip support not yet implemented"
                raise NotImplementedError(msg)
            value = self._pack("L", self._unpack("L", value)[0] + offset)
            entries[stripoffsets] = tag, typ, count, value, data

        # pass 2: write entries to file
        for tag, typ, count, value, data in entries:
            logger.debug(f"{tag} {typ} {count} {repr(value)} {repr(data)}")
            result += self._pack("HHL4s", tag, typ, count, value)

        # -- overwrite here for multi-page --
        result += b"\0\0\0\0"  # end of entries

        # pass 3: write auxiliary data to file
        for tag, typ, count, value, data in entries:
            result += data
            if len(data) & 1:
                result += b"\0"

        return result
