    def load(self) -> Image.core.PixelAccess | None:
        if self.tile and self._reduce:
            power = 1 << self._reduce
            adjust = power >> 1
            self._size = (
                int((self.size[0] + adjust) / power),
                int((self.size[1] + adjust) / power),
            )

            # Update the reduce and layers settings
            t = self.tile[0]
            assert isinstance(t[3], tuple)
            t3 = (t[3][0], self._reduce, self.layers, t[3][3], t[3][4])
            self.tile = [ImageFile._Tile(t[0], (0, 0) + self.size, t[2], t3)]

        return ImageFile.ImageFile.load(self)
