    def _open_index(self, index: int = 1) -> None:
        #
        # get the Image Contents Property Set

        prop = self.ole.getproperties(
            [f"Data Object Store {index:06d}", "\005Image Contents"]
        )

        # size (highest resolution)

        self._size = prop[0x1000002], prop[0x1000003]

        size = max(self.size)
        i = 1
        while size > 64:
            size = size // 2
            i += 1
        self.maxid = i - 1

        # mode.  instead of using a single field for this, flashpix
        # requires you to specify the mode for each channel in each
        # resolution subimage, and leaves it to the decoder to make
        # sure that they all match.  for now, we'll cheat and assume
        # that this is always the case.

        id = self.maxid << 16

        s = prop[0x2000002 | id]

        bands = i32(s, 4)
        if bands > 4:
            msg = "Invalid number of bands"
            raise OSError(msg)

        # note: for now, we ignore the "uncalibrated" flag
        colors = tuple(i32(s, 8 + i * 4) & 0x7FFFFFFF for i in range(bands))

        self._mode, self.rawmode = MODES[colors]

        # load JPEG tables, if any
        self.jpeg = {}
        for i in range(256):
            id = 0x3000001 | (i << 16)
            if id in prop:
                self.jpeg[i] = prop[id]

        self._open_subimage(1, self.maxid)
