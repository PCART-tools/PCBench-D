    def _open(self) -> None:
        assert self.fp is not None

        magic_number = self._read_magic()
        try:
            mode = MODES[magic_number]
        except KeyError:
            msg = "not a PPM file"
            raise SyntaxError(msg)
        self._mode = mode

        if magic_number in (b"P1", b"P4"):
            self.custom_mimetype = "image/x-portable-bitmap"
        elif magic_number in (b"P2", b"P5"):
            self.custom_mimetype = "image/x-portable-graymap"
        elif magic_number in (b"P3", b"P6"):
            self.custom_mimetype = "image/x-portable-pixmap"

        self._size = int(self._read_token()), int(self._read_token())

        decoder_name = "raw"
        if magic_number in (b"P1", b"P2", b"P3"):
            decoder_name = "ppm_plain"

        args: str | tuple[str | int, ...]
        if mode == "1":
            args = "1;I"
        elif mode == "F":
            scale = float(self._read_token())
            if scale == 0.0 or not math.isfinite(scale):
                msg = "scale must be finite and non-zero"
                raise ValueError(msg)
            self.info["scale"] = abs(scale)

            rawmode = "F;32F" if scale < 0 else "F;32BF"
            args = (rawmode, 0, -1)
        else:
            maxval = int(self._read_token())
            if not 0 < maxval < 65536:
                msg = "maxval must be greater than 0 and less than 65536"
                raise ValueError(msg)
            if maxval > 255 and mode == "L":
                self._mode = "I"

            rawmode = mode
            if decoder_name != "ppm_plain":
                # If maxval matches a bit depth, use the raw decoder directly
                if maxval == 65535 and mode == "L":
                    rawmode = "I;16B"
                elif maxval != 255:
                    decoder_name = "ppm"

            args = rawmode if decoder_name == "raw" else (rawmode, maxval)
        self.tile = [(decoder_name, (0, 0) + self.size, self.fp.tell(), args)]
