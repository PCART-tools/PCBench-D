    def compile(self):
        """Create metrics and bitmap"""

        if self.bitmap:
            return

        # create bitmap large enough to hold all data
        h = w = maxwidth = 0
        lines = 1
        for glyph in self:
            if glyph:
                d, dst, src, im = glyph
                h = max(h, src[3] - src[1])
                w = w + (src[2] - src[0])
                if w > WIDTH:
                    lines += 1
                    w = src[2] - src[0]
                maxwidth = max(maxwidth, w)

        xsize = maxwidth
        ysize = lines * h

        if xsize == 0 and ysize == 0:
            return ""

        self.ysize = h

        # paste glyphs into bitmap
        self.bitmap = Image.new("1", (xsize, ysize))
        self.metrics = [None] * 256
        x = y = 0
        for i in range(256):
            glyph = self[i]
            if glyph:
                d, dst, src, im = glyph
                xx = src[2] - src[0]
                # yy = src[3] - src[1]
                x0, y0 = x, y
                x = x + xx
                if x > WIDTH:
                    x, y = 0, y + h
                    x0, y0 = x, y
                    x = xx
                s = src[0] + x0, src[1] + y0, src[2] + x0, src[3] + y0
                self.bitmap.paste(im.crop(src), s)
                self.metrics[i] = d, dst, s
