    def _open_subimage(self, index: int = 1, subimage: int = 0) -> None:
        #
        # setup tile descriptors for a given subimage

        stream = [
            f"Data Object Store {index:06d}",
            f"Resolution {subimage:04d}",
            "Subimage 0000 Header",
        ]

        fp = self.ole.openstream(stream)

        # skip prefix
        fp.read(28)

        # header stream
        s = fp.read(36)

        size = i32(s, 4), i32(s, 8)
        # tilecount = i32(s, 12)
        tilesize = i32(s, 16), i32(s, 20)
        # channels = i32(s, 24)
        offset = i32(s, 28)
        length = i32(s, 32)

        if size != self.size:
            msg = "subimage mismatch"
            raise OSError(msg)

        # get tile descriptors
        fp.seek(28 + offset)
        s = fp.read(i32(s, 12) * length)

        x = y = 0
        xsize, ysize = size
        xtile, ytile = tilesize
        self.tile = []

        for i in range(0, len(s), length):
            x1 = min(xsize, x + xtile)
            y1 = min(ysize, y + ytile)

            compression = i32(s, i + 8)

            if compression == 0:
                self.tile.append(
                    ImageFile._Tile(
                        "raw",
                        (x, y, x1, y1),
                        i32(s, i) + 28,
                        self.rawmode,
                    )
                )

            elif compression == 1:
                # FIXME: the fill decoder is not implemented
                self.tile.append(
                    ImageFile._Tile(
                        "fill",
                        (x, y, x1, y1),
                        i32(s, i) + 28,
                        (self.rawmode, s[12:16]),
                    )
                )

            elif compression == 2:
                internal_color_conversion = s[14]
                jpeg_tables = s[15]
                rawmode = self.rawmode

                if internal_color_conversion:
                    # The image is stored as usual (usually YCbCr).
                    if rawmode == "RGBA":
                        # For "RGBA", data is stored as YCbCrA based on
                        # negative RGB. The following trick works around
                        # this problem :
                        jpegmode, rawmode = "YCbCrK", "CMYK"
                    else:
                        jpegmode = None  # let the decoder decide

                else:
                    # The image is stored as defined by rawmode
                    jpegmode = rawmode

                self.tile.append(
                    ImageFile._Tile(
                        "jpeg",
                        (x, y, x1, y1),
                        i32(s, i) + 28,
                        (rawmode, jpegmode),
                    )
                )

                # FIXME: jpeg tables are tile dependent; the prefix
                # data must be placed in the tile descriptor itself!

                if jpeg_tables:
                    self.tile_prefix = self.jpeg[jpeg_tables]

            else:
                msg = "unknown/invalid compression"
                raise OSError(msg)

            x = x + xtile
            if x >= xsize:
                x, y = 0, y + ytile
                if y >= ysize:
                    break  # isn't really required

        self.stream = stream
        self._fp = self.fp
        self.fp = None
