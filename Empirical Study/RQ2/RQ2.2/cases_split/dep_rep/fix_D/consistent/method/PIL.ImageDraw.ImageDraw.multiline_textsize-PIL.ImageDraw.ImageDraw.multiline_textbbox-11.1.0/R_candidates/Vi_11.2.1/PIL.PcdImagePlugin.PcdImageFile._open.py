    def _open(self) -> None:
        # rough
        assert self.fp is not None

        self.fp.seek(2048)
        s = self.fp.read(2048)

        if not s.startswith(b"PCD_"):
            msg = "not a PCD file"
            raise SyntaxError(msg)

        orientation = s[1538] & 3
        self.tile_post_rotate = None
        if orientation == 1:
            self.tile_post_rotate = 90
        elif orientation == 3:
            self.tile_post_rotate = -90

        self._mode = "RGB"
        self._size = 768, 512  # FIXME: not correct for rotated images!
        self.tile = [ImageFile._Tile("pcd", (0, 0) + self.size, 96 * 2048)]
