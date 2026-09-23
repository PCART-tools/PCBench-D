    def _open(self) -> None:
        # Quick rejection: if there's not an LF among the first
        # 100 bytes, this is (probably) not a text header.

        if b"\n" not in self.fp.read(100):
            msg = "not an IM file"
            raise SyntaxError(msg)
        self.fp.seek(0)

        n = 0

        # Default values
        self.info[MODE] = "L"
        self.info[SIZE] = (512, 512)
        self.info[FRAMES] = 1

        self.rawmode = "L"

        while True:
            s = self.fp.read(1)

            # Some versions of IFUNC uses \n\r instead of \r\n...
            if s == b"\r":
                continue

            if not s or s == b"\0" or s == b"\x1A":
                break

            # FIXME: this may read whole file if not a text file
            s = s + self.fp.readline()

            if len(s) > 100:
                msg = "not an IM file"
                raise SyntaxError(msg)

            if s[-2:] == b"\r\n":
                s = s[:-2]
            elif s[-1:] == b"\n":
                s = s[:-1]

            try:
                m = split.match(s)
            except re.error as e:
                msg = "not an IM file"
                raise SyntaxError(msg) from e

            if m:
                k, v = m.group(1, 2)

                # Don't know if this is the correct encoding,
                # but a decent guess (I guess)
                k = k.decode("latin-1", "replace")
                v = v.decode("latin-1", "replace")

                # Convert value as appropriate
                if k in [FRAMES, SCALE, SIZE]:
                    v = v.replace("*", ",")
                    v = tuple(map(number, v.split(",")))
                    if len(v) == 1:
                        v = v[0]
                elif k == MODE and v in OPEN:
                    v, self.rawmode = OPEN[v]

                # Add to dictionary. Note that COMMENT tags are
                # combined into a list of strings.
                if k == COMMENT:
                    if k in self.info:
                        self.info[k].append(v)
                    else:
                        self.info[k] = [v]
                else:
                    self.info[k] = v

                if k in TAGS:
                    n += 1

            else:
                msg = f"Syntax error in IM header: {s.decode('ascii', 'replace')}"
                raise SyntaxError(msg)

        if not n:
            msg = "Not an IM file"
            raise SyntaxError(msg)

        # Basic attributes
        self._size = self.info[SIZE]
        self._mode = self.info[MODE]

        # Skip forward to start of image data
        while s and s[:1] != b"\x1A":
            s = self.fp.read(1)
        if not s:
            msg = "File truncated"
            raise SyntaxError(msg)

        if LUT in self.info:
            # convert lookup table to palette or lut attribute
            palette = self.fp.read(768)
            greyscale = 1  # greyscale palette
            linear = 1  # linear greyscale palette
            for i in range(256):
                if palette[i] == palette[i + 256] == palette[i + 512]:
                    if palette[i] != i:
                        linear = 0
                else:
                    greyscale = 0
            if self.mode in ["L", "LA", "P", "PA"]:
                if greyscale:
                    if not linear:
                        self.lut = list(palette[:256])
                else:
                    if self.mode in ["L", "P"]:
                        self._mode = self.rawmode = "P"
                    elif self.mode in ["LA", "PA"]:
                        self._mode = "PA"
                        self.rawmode = "PA;L"
                    self.palette = ImagePalette.raw("RGB;L", palette)
            elif self.mode == "RGB":
                if not greyscale or not linear:
                    self.lut = list(palette)

        self.frame = 0

        self.__offset = offs = self.fp.tell()

        self._fp = self.fp  # FIXME: hack

        if self.rawmode[:2] == "F;":
            # ifunc95 formats
            try:
                # use bit decoder (if necessary)
                bits = int(self.rawmode[2:])
                if bits not in [8, 16, 32]:
                    self.tile = [
                        ImageFile._Tile(
                            "bit", (0, 0) + self.size, offs, (bits, 8, 3, 0, -1)
                        )
                    ]
                    return
            except ValueError:
                pass

        if self.rawmode in ["RGB;T", "RYB;T"]:
            # Old LabEye/3PC files.  Would be very surprised if anyone
            # ever stumbled upon such a file ;-)
            size = self.size[0] * self.size[1]
            self.tile = [
                ImageFile._Tile("raw", (0, 0) + self.size, offs, ("G", 0, -1)),
                ImageFile._Tile("raw", (0, 0) + self.size, offs + size, ("R", 0, -1)),
                ImageFile._Tile(
                    "raw", (0, 0) + self.size, offs + 2 * size, ("B", 0, -1)
                ),
            ]
        else:
            # LabEye/IFUNC files
            self.tile = [
                ImageFile._Tile("raw", (0, 0) + self.size, offs, (self.rawmode, 0, -1))
            ]
