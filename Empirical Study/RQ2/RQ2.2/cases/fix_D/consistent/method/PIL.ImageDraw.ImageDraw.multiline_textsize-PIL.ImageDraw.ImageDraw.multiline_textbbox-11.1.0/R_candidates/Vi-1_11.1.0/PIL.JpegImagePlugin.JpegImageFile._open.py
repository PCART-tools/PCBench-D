    def _open(self) -> None:
        s = self.fp.read(3)

        if not _accept(s):
            msg = "not a JPEG file"
            raise SyntaxError(msg)
        s = b"\xFF"

        # Create attributes
        self.bits = self.layers = 0
        self._exif_offset = 0

        # JPEG specifics (internal)
        self.layer: list[tuple[int, int, int, int]] = []
        self._huffman_dc: dict[Any, Any] = {}
        self._huffman_ac: dict[Any, Any] = {}
        self.quantization: dict[int, list[int]] = {}
        self.app: dict[str, bytes] = {}  # compatibility
        self.applist: list[tuple[str, bytes]] = []
        self.icclist: list[bytes] = []

        while True:
            i = s[0]
            if i == 0xFF:
                s = s + self.fp.read(1)
                i = i16(s)
            else:
                # Skip non-0xFF junk
                s = self.fp.read(1)
                continue

            if i in MARKER:
                name, description, handler = MARKER[i]
                if handler is not None:
                    handler(self, i)
                if i == 0xFFDA:  # start of scan
                    rawmode = self.mode
                    if self.mode == "CMYK":
                        rawmode = "CMYK;I"  # assume adobe conventions
                    self.tile = [
                        ImageFile._Tile("jpeg", (0, 0) + self.size, 0, (rawmode, ""))
                    ]
                    # self.__offset = self.fp.tell()
                    break
                s = self.fp.read(1)
            elif i in {0, 0xFFFF}:
                # padded marker or junk; move on
                s = b"\xff"
            elif i == 0xFF00:  # Skip extraneous data (escaped 0xFF)
                s = self.fp.read(1)
            else:
                msg = "no marker found"
                raise SyntaxError(msg)

        self._read_dpi_from_exif()
