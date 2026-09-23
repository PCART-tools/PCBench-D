    def _open(self):
        magic_number = self._read_magic()
        try:
            mode = MODES[magic_number]
        except KeyError:
            msg = "not a PPM file"
            raise SyntaxError(msg)

        if magic_number in (b"P1", b"P4"):
            self.custom_mimetype = "image/x-portable-bitmap"
        elif magic_number in (b"P2", b"P5"):
            self.custom_mimetype = "image/x-portable-graymap"
        elif magic_number in (b"P3", b"P6"):
            self.custom_mimetype = "image/x-portable-pixmap"

        maxval = None
        decoder_name = "raw"
        if magic_number in (b"P1", b"P2", b"P3"):
            decoder_name = "ppm_plain"
        for ix in range(3):
            token = int(self._read_token())
            if ix == 0:  # token is the x size
                xsize = token
            elif ix == 1:  # token is the y size
                ysize = token
                if mode == "1":
                    self._mode = "1"
                    rawmode = "1;I"
                    break
                else:
                    self._mode = rawmode = mode
            elif ix == 2:  # token is maxval
                maxval = token
                if not 0 < maxval < 65536:
                    msg = "maxval must be greater than 0 and less than 65536"
                    raise ValueError(msg)
                if maxval > 255 and mode == "L":
                    self._mode = "I"

                if decoder_name != "ppm_plain":
                    # If maxval matches a bit depth, use the raw decoder directly
                    if maxval == 65535 and mode == "L":
                        rawmode = "I;16B"
                    elif maxval != 255:
                        decoder_name = "ppm"

        args = (rawmode, 0, 1) if decoder_name == "raw" else (rawmode, maxval)
        self._size = xsize, ysize
        self.tile = [(decoder_name, (0, 0, xsize, ysize), self.fp.tell(), args)]
