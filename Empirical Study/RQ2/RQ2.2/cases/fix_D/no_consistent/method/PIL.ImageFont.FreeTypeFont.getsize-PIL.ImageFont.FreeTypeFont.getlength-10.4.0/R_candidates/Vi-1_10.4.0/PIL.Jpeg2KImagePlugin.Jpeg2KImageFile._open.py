    def _open(self) -> None:
        sig = self.fp.read(4)
        if sig == b"\xff\x4f\xff\x51":
            self.codec = "j2k"
            self._size, self._mode = _parse_codestream(self.fp)
        else:
            sig = sig + self.fp.read(8)

            if sig == b"\x00\x00\x00\x0cjP  \x0d\x0a\x87\x0a":
                self.codec = "jp2"
                header = _parse_jp2_header(self.fp)
                self._size, self._mode, self.custom_mimetype, dpi, self.palette = header
                if dpi is not None:
                    self.info["dpi"] = dpi
                if self.fp.read(12).endswith(b"jp2c\xff\x4f\xff\x51"):
                    self._parse_comment()
            else:
                msg = "not a JPEG 2000 file"
                raise SyntaxError(msg)

        self._reduce = 0
        self.layers = 0

        fd = -1
        length = -1

        try:
            fd = self.fp.fileno()
            length = os.fstat(fd).st_size
        except Exception:
            fd = -1
            try:
                pos = self.fp.tell()
                self.fp.seek(0, io.SEEK_END)
                length = self.fp.tell()
                self.fp.seek(pos)
            except Exception:
                length = -1

        self.tile = [
            (
                "jpeg2k",
                (0, 0) + self.size,
                0,
                (self.codec, self._reduce, self.layers, fd, length),
            )
        ]
