    def load(self, fp: IO[bytes]) -> None:
        self.reset()
        self._offset = fp.tell()

        try:
            tag_count = (
                self._unpack("Q", self._ensure_read(fp, 8))
                if self._bigtiff
                else self._unpack("H", self._ensure_read(fp, 2))
            )[0]
            for i in range(tag_count):
                tag, typ, count, data = (
                    self._unpack("HHQ8s", self._ensure_read(fp, 20))
                    if self._bigtiff
                    else self._unpack("HHL4s", self._ensure_read(fp, 12))
                )

                tagname = TiffTags.lookup(tag, self.group).name
                typname = TYPES.get(typ, "unknown")
                msg = f"tag: {tagname} ({tag}) - type: {typname} ({typ})"

                try:
                    unit_size, handler = self._load_dispatch[typ]
                except KeyError:
                    logger.debug("%s - unsupported type %s", msg, typ)
                    continue  # ignore unsupported type
                size = count * unit_size
                if size > (8 if self._bigtiff else 4):
                    here = fp.tell()
                    (offset,) = self._unpack("Q" if self._bigtiff else "L", data)
                    msg += f" Tag Location: {here} - Data Location: {offset}"
                    fp.seek(offset)
                    data = ImageFile._safe_read(fp, size)
                    fp.seek(here)
                else:
                    data = data[:size]

                if len(data) != size:
                    warnings.warn(
                        "Possibly corrupt EXIF data.  "
                        f"Expecting to read {size} bytes but only got {len(data)}."
                        f" Skipping tag {tag}"
                    )
                    logger.debug(msg)
                    continue

                if not data:
                    logger.debug(msg)
                    continue

                self._tagdata[tag] = data
                self.tagtype[tag] = typ

                msg += " - value: " + (
                    "<table: %d bytes>" % size if size > 32 else repr(data)
                )
                logger.debug(msg)

            (self.next,) = (
                self._unpack("Q", self._ensure_read(fp, 8))
                if self._bigtiff
                else self._unpack("L", self._ensure_read(fp, 4))
            )
        except OSError as msg:
            warnings.warn(str(msg))
            return
