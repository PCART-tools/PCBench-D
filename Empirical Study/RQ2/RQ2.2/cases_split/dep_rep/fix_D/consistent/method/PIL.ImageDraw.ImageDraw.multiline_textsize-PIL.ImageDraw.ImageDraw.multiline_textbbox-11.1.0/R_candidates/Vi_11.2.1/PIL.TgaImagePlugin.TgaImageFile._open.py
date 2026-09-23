    def _open(self) -> None:
        # process header
        assert self.fp is not None

        s = self.fp.read(18)

        id_len = s[0]

        colormaptype = s[1]
        imagetype = s[2]

        depth = s[16]

        flags = s[17]

        self._size = i16(s, 12), i16(s, 14)

        # validate header fields
        if (
            colormaptype not in (0, 1)
            or self.size[0] <= 0
            or self.size[1] <= 0
            or depth not in (1, 8, 16, 24, 32)
        ):
            msg = "not a TGA file"
            raise SyntaxError(msg)

        # image mode
        if imagetype in (3, 11):
            self._mode = "L"
            if depth == 1:
                self._mode = "1"  # ???
            elif depth == 16:
                self._mode = "LA"
        elif imagetype in (1, 9):
            self._mode = "P" if colormaptype else "L"
        elif imagetype in (2, 10):
            self._mode = "RGB" if depth == 24 else "RGBA"
        else:
            msg = "unknown TGA mode"
            raise SyntaxError(msg)

        # orientation
        orientation = flags & 0x30
        self._flip_horizontally = orientation in [0x10, 0x30]
        if orientation in [0x20, 0x30]:
            orientation = 1
        elif orientation in [0, 0x10]:
            orientation = -1
        else:
            msg = "unknown TGA orientation"
            raise SyntaxError(msg)

        self.info["orientation"] = orientation

        if imagetype & 8:
            self.info["compression"] = "tga_rle"

        if id_len:
            self.info["id_section"] = self.fp.read(id_len)

        if colormaptype:
            # read palette
            start, size, mapdepth = i16(s, 3), i16(s, 5), s[7]
            if mapdepth == 16:
                self.palette = ImagePalette.raw(
                    "BGRA;15Z", bytes(2 * start) + self.fp.read(2 * size)
                )
                self.palette.mode = "RGBA"
            elif mapdepth == 24:
                self.palette = ImagePalette.raw(
                    "BGR", bytes(3 * start) + self.fp.read(3 * size)
                )
            elif mapdepth == 32:
                self.palette = ImagePalette.raw(
                    "BGRA", bytes(4 * start) + self.fp.read(4 * size)
                )
            else:
                msg = "unknown TGA map depth"
                raise SyntaxError(msg)

        # setup tile descriptor
        try:
            rawmode = MODES[(imagetype & 7, depth)]
            if imagetype & 8:
                # compressed
                self.tile = [
                    ImageFile._Tile(
                        "tga_rle",
                        (0, 0) + self.size,
                        self.fp.tell(),
                        (rawmode, orientation, depth),
                    )
                ]
            else:
                self.tile = [
                    ImageFile._Tile(
                        "raw",
                        (0, 0) + self.size,
                        self.fp.tell(),
                        (rawmode, 0, orientation),
                    )
                ]
        except KeyError:
            pass  # cannot decode
