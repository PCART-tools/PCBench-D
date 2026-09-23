    def _open(self) -> None:
        # HEAD
        assert self.fp is not None

        headlen = 512
        s = self.fp.read(headlen)

        if not _accept(s):
            msg = "Not an SGI image file"
            raise ValueError(msg)

        # compression : verbatim or RLE
        compression = s[2]

        # bpc : 1 or 2 bytes (8bits or 16bits)
        bpc = s[3]

        # dimension : 1, 2 or 3 (depending on xsize, ysize and zsize)
        dimension = i16(s, 4)

        # xsize : width
        xsize = i16(s, 6)

        # ysize : height
        ysize = i16(s, 8)

        # zsize : channels count
        zsize = i16(s, 10)

        # layout
        layout = bpc, dimension, zsize

        # determine mode from bits/zsize
        rawmode = ""
        try:
            rawmode = MODES[layout]
        except KeyError:
            pass

        if rawmode == "":
            msg = "Unsupported SGI image mode"
            raise ValueError(msg)

        self._size = xsize, ysize
        self._mode = rawmode.split(";")[0]
        if self.mode == "RGB":
            self.custom_mimetype = "image/rgb"

        # orientation -1 : scanlines begins at the bottom-left corner
        orientation = -1

        # decoder info
        if compression == 0:
            pagesize = xsize * ysize * bpc
            if bpc == 2:
                self.tile = [
                    ImageFile._Tile(
                        "SGI16",
                        (0, 0) + self.size,
                        headlen,
                        (self.mode, 0, orientation),
                    )
                ]
            else:
                self.tile = []
                offset = headlen
                for layer in self.mode:
                    self.tile.append(
                        ImageFile._Tile(
                            "raw", (0, 0) + self.size, offset, (layer, 0, orientation)
                        )
                    )
                    offset += pagesize
        elif compression == 1:
            self.tile = [
                ImageFile._Tile(
                    "sgi_rle", (0, 0) + self.size, headlen, (rawmode, orientation, bpc)
                )
            ]
