    def decode(self, buffer: bytes) -> tuple[int, int]:
        assert self.fd is not None

        self._previously_seen_pixels = {}
        self._add_to_previous_pixels(bytearray((0, 0, 0, 255)))

        data = bytearray()
        bands = Image.getmodebands(self.mode)
        dest_length = self.state.xsize * self.state.ysize * bands
        while len(data) < dest_length:
            byte = self.fd.read(1)[0]
            value: bytes | bytearray
            if byte == 0b11111110 and self._previous_pixel:  # QOI_OP_RGB
                value = bytearray(self.fd.read(3)) + self._previous_pixel[3:]
            elif byte == 0b11111111:  # QOI_OP_RGBA
                value = self.fd.read(4)
            else:
                op = byte >> 6
                if op == 0:  # QOI_OP_INDEX
                    op_index = byte & 0b00111111
                    value = self._previously_seen_pixels.get(
                        op_index, bytearray((0, 0, 0, 0))
                    )
                elif op == 1 and self._previous_pixel:  # QOI_OP_DIFF
                    value = bytearray(
                        (
                            (self._previous_pixel[0] + ((byte & 0b00110000) >> 4) - 2)
                            % 256,
                            (self._previous_pixel[1] + ((byte & 0b00001100) >> 2) - 2)
                            % 256,
                            (self._previous_pixel[2] + (byte & 0b00000011) - 2) % 256,
                            self._previous_pixel[3],
                        )
                    )
                elif op == 2 and self._previous_pixel:  # QOI_OP_LUMA
                    second_byte = self.fd.read(1)[0]
                    diff_green = (byte & 0b00111111) - 32
                    diff_red = ((second_byte & 0b11110000) >> 4) - 8
                    diff_blue = (second_byte & 0b00001111) - 8

                    value = bytearray(
                        tuple(
                            (self._previous_pixel[i] + diff_green + diff) % 256
                            for i, diff in enumerate((diff_red, 0, diff_blue))
                        )
                    )
                    value += self._previous_pixel[3:]
                elif op == 3 and self._previous_pixel:  # QOI_OP_RUN
                    run_length = (byte & 0b00111111) + 1
                    value = self._previous_pixel
                    if bands == 3:
                        value = value[:3]
                    data += value * run_length
                    continue
            self._add_to_previous_pixels(value)

            if bands == 3:
                value = value[:3]
            data += value
        self.set_as_raw(data)
        return -1, 0
