    def tobytes(self, offset: int = 0) -> bytes:
        # FIXME What about tagdata?
        result = self._pack("Q" if self._bigtiff else "H", len(self._tags_v2))

        entries: list[tuple[int, int, int, bytes, bytes]] = []

        fmt = "Q" if self._bigtiff else "L"
        fmt_size = 8 if self._bigtiff else 4
        offset += (
            len(result) + len(self._tags_v2) * (20 if self._bigtiff else 12) + fmt_size
        )
        stripoffsets = None

        # pass 1: convert tags to binary format
        # always write tags in ascending order
        for tag, value in sorted(self._tags_v2.items()):
            if tag == STRIPOFFSETS:
                stripoffsets = len(entries)
            typ = self.tagtype[tag]
            logger.debug("Tag %s, Type: %s, Value: %s", tag, typ, repr(value))
            is_ifd = typ == TiffTags.LONG and isinstance(value, dict)
            if is_ifd:
                ifd = ImageFileDirectory_v2(self._get_ifh(), group=tag)
                values = self._tags_v2[tag]
                for ifd_tag, ifd_value in values.items():
                    ifd[ifd_tag] = ifd_value
                data = ifd.tobytes(offset)
            else:
                values = value if isinstance(value, tuple) else (value,)
                data = self._write_dispatch[typ](self, *values)

            tagname = TiffTags.lookup(tag, self.group).name
            typname = "ifd" if is_ifd else TYPES.get(typ, "unknown")
            msg = f"save: {tagname} ({tag}) - type: {typname} ({typ}) - value: "
            msg += f"<table: {len(data)} bytes>" if len(data) >= 16 else str(values)
            logger.debug(msg)

            # count is sum of lengths for string and arbitrary data
            if is_ifd:
                count = 1
            elif typ in [TiffTags.BYTE, TiffTags.ASCII, TiffTags.UNDEFINED]:
                count = len(data)
            else:
                count = len(values)
            # figure out if data fits into the entry
            if len(data) <= fmt_size:
                entries.append((tag, typ, count, data.ljust(fmt_size, b"\0"), b""))
            else:
                entries.append((tag, typ, count, self._pack(fmt, offset), data))
                offset += (len(data) + 1) // 2 * 2  # pad to word

        # update strip offset data to point beyond auxiliary data
        if stripoffsets is not None:
            tag, typ, count, value, data = entries[stripoffsets]
            if data:
                size, handler = self._load_dispatch[typ]
                values = [val + offset for val in handler(self, data, self.legacy_api)]
                data = self._write_dispatch[typ](self, *values)
            else:
                value = self._pack(fmt, self._unpack(fmt, value)[0] + offset)
            entries[stripoffsets] = tag, typ, count, value, data

        # pass 2: write entries to file
        for tag, typ, count, value, data in entries:
            logger.debug("%s %s %s %s %s", tag, typ, count, repr(value), repr(data))
            result += self._pack(
                "HHQ8s" if self._bigtiff else "HHL4s", tag, typ, count, value
            )

        # -- overwrite here for multi-page --
        result += self._pack(fmt, 0)  # end of entries

        # pass 3: write auxiliary data to file
        for tag, typ, count, value, data in entries:
            result += data
            if len(data) & 1:
                result += b"\0"

        return result
