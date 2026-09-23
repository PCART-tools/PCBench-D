    def decode(self, buffer: bytes | Image.SupportsArrayInterface) -> tuple[int, int]:
        assert self.fd is not None

        data = bytearray()
        maxval = self.args[-1]
        in_byte_count = 1 if maxval < 256 else 2
        out_byte_count = 4 if self.mode == "I" else 1
        out_max = 65535 if self.mode == "I" else 255
        bands = Image.getmodebands(self.mode)
        dest_length = self.state.xsize * self.state.ysize * bands * out_byte_count
        while len(data) < dest_length:
            pixels = self.fd.read(in_byte_count * bands)
            if len(pixels) < in_byte_count * bands:
                # eof
                break
            for b in range(bands):
                value = (
                    pixels[b] if in_byte_count == 1 else i16(pixels, b * in_byte_count)
                )
                value = min(out_max, round(value / maxval * out_max))
                data += o32(value) if self.mode == "I" else o8(value)
        rawmode = "I;32" if self.mode == "I" else self.mode
        self.set_as_raw(bytes(data), rawmode)
        return -1, 0
