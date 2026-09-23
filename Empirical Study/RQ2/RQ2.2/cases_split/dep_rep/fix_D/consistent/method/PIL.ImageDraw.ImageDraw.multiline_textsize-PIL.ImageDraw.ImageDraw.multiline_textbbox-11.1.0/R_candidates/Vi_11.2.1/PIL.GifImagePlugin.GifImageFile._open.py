    def _open(self) -> None:
        # Screen
        s = self.fp.read(13)
        if not _accept(s):
            msg = "not a GIF file"
            raise SyntaxError(msg)

        self.info["version"] = s[:6]
        self._size = i16(s, 6), i16(s, 8)
        flags = s[10]
        bits = (flags & 7) + 1

        if flags & 128:
            # get global palette
            self.info["background"] = s[11]
            # check if palette contains colour indices
            p = self.fp.read(3 << bits)
            if self._is_palette_needed(p):
                p = ImagePalette.raw("RGB", p)
                self.global_palette = self.palette = p

        self._fp = self.fp  # FIXME: hack
        self.__rewind = self.fp.tell()
        self._n_frames: int | None = None
        self._seek(0)  # get ready to read first frame
