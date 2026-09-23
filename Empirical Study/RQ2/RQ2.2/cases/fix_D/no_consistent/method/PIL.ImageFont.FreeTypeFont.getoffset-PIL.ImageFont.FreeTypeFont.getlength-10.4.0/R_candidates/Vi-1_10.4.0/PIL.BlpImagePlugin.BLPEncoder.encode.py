    def encode(self, bufsize: int) -> tuple[int, int, bytes]:
        palette_data = self._write_palette()

        offset = 20 + 16 * 4 * 2 + len(palette_data)
        data = struct.pack("<16I", offset, *((0,) * 15))

        assert self.im is not None
        w, h = self.im.size
        data += struct.pack("<16I", w * h, *((0,) * 15))

        data += palette_data

        for y in range(h):
            for x in range(w):
                data += struct.pack("<B", self.im.getpixel((x, y)))

        return len(data), 0, data
