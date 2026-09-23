    def _write_palette(self):
        data = b""
        palette = self.im.getpalette("RGBA", "RGBA")
        for i in range(256):
            r, g, b, a = palette[i * 4 : (i + 1) * 4]
            data += struct.pack("<4B", b, g, r, a)
        return data
