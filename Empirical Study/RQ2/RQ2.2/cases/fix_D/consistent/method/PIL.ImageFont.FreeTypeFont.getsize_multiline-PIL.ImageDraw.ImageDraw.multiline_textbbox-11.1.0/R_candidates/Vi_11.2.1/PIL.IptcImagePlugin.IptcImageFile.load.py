    def load(self) -> Image.core.PixelAccess | None:
        if len(self.tile) != 1 or self.tile[0][0] != "iptc":
            return ImageFile.ImageFile.load(self)

        offset, compression = self.tile[0][2:]

        self.fp.seek(offset)

        # Copy image data to temporary file
        o = BytesIO()
        if compression == "raw":
            # To simplify access to the extracted file,
            # prepend a PPM header
            o.write(b"P5\n%d %d\n255\n" % self.size)
        while True:
            type, size = self.field()
            if type != (8, 10):
                break
            while size > 0:
                s = self.fp.read(min(size, 8192))
                if not s:
                    break
                o.write(s)
                size -= len(s)

        with Image.open(o) as _im:
            _im.load()
            self.im = _im.im
        return None
