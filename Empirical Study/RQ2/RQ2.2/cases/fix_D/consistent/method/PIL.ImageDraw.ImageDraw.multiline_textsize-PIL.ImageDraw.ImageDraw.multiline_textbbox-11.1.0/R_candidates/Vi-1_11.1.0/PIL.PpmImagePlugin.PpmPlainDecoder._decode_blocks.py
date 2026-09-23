    def _decode_blocks(self, maxval: int) -> bytearray:
        data = bytearray()
        max_len = 10
        out_byte_count = 4 if self.mode == "I" else 1
        out_max = 65535 if self.mode == "I" else 255
        bands = Image.getmodebands(self.mode)
        total_bytes = self.state.xsize * self.state.ysize * bands * out_byte_count

        half_token = b""
        while len(data) != total_bytes:
            block = self._read_block()  # read next block
            if not block:
                if half_token:
                    block = bytearray(b" ")  # flush half_token
                else:
                    # eof
                    break

            block = self._ignore_comments(block)

            if half_token:
                block = half_token + block  # stitch half_token to new block
                half_token = b""

            tokens = block.split()

            if block and not block[-1:].isspace():  # block might split token
                half_token = tokens.pop()  # save half token for later
                if len(half_token) > max_len:  # prevent buildup of half_token
                    msg = (
                        b"Token too long found in data: %s" % half_token[: max_len + 1]
                    )
                    raise ValueError(msg)

            for token in tokens:
                if len(token) > max_len:
                    msg = b"Token too long found in data: %s" % token[: max_len + 1]
                    raise ValueError(msg)
                value = int(token)
                if value < 0:
                    msg_str = f"Channel value is negative: {value}"
                    raise ValueError(msg_str)
                if value > maxval:
                    msg_str = f"Channel value too large for this mode: {value}"
                    raise ValueError(msg_str)
                value = round(value / maxval * out_max)
                data += o32(value) if self.mode == "I" else o8(value)
                if len(data) == total_bytes:  # finished!
                    break
        return data
