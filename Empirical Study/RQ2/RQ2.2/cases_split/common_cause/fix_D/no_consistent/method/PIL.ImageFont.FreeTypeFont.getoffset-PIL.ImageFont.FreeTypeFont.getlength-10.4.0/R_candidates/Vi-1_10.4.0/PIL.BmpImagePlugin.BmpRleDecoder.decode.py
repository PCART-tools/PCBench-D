    def decode(self, buffer: bytes) -> tuple[int, int]:
        assert self.fd is not None
        rle4 = self.args[1]
        data = bytearray()
        x = 0
        dest_length = self.state.xsize * self.state.ysize
        while len(data) < dest_length:
            pixels = self.fd.read(1)
            byte = self.fd.read(1)
            if not pixels or not byte:
                break
            num_pixels = pixels[0]
            if num_pixels:
                # encoded mode
                if x + num_pixels > self.state.xsize:
                    # Too much data for row
                    num_pixels = max(0, self.state.xsize - x)
                if rle4:
                    first_pixel = o8(byte[0] >> 4)
                    second_pixel = o8(byte[0] & 0x0F)
                    for index in range(num_pixels):
                        if index % 2 == 0:
                            data += first_pixel
                        else:
                            data += second_pixel
                else:
                    data += byte * num_pixels
                x += num_pixels
            else:
                if byte[0] == 0:
                    # end of line
                    while len(data) % self.state.xsize != 0:
                        data += b"\x00"
                    x = 0
                elif byte[0] == 1:
                    # end of bitmap
                    break
                elif byte[0] == 2:
                    # delta
                    bytes_read = self.fd.read(2)
                    if len(bytes_read) < 2:
                        break
                    right, up = self.fd.read(2)
                    data += b"\x00" * (right + up * self.state.xsize)
                    x = len(data) % self.state.xsize
                else:
                    # absolute mode
                    if rle4:
                        # 2 pixels per byte
                        byte_count = byte[0] // 2
                        bytes_read = self.fd.read(byte_count)
                        for byte_read in bytes_read:
                            data += o8(byte_read >> 4)
                            data += o8(byte_read & 0x0F)
                    else:
                        byte_count = byte[0]
                        bytes_read = self.fd.read(byte_count)
                        data += bytes_read
                    if len(bytes_read) < byte_count:
                        break
                    x += byte[0]

                    # align to 16-bit word boundary
                    if self.fd.tell() % 2 != 0:
                        self.fd.seek(1, os.SEEK_CUR)
        rawmode = "L" if self.mode == "L" else "P"
        self.set_as_raw(bytes(data), (rawmode, 0, self.args[-1]))
        return -1, 0
