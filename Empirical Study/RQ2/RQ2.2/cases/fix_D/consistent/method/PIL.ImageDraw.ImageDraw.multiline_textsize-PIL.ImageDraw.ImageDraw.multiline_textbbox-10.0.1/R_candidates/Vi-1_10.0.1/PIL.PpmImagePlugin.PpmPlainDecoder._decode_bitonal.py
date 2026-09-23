    def _decode_bitonal(self):
        """
        This is a separate method because in the plain PBM format, all data tokens are
        exactly one byte, so the inter-token whitespace is optional.
        """
        data = bytearray()
        total_bytes = self.state.xsize * self.state.ysize

        while len(data) != total_bytes:
            block = self._read_block()  # read next block
            if not block:
                # eof
                break

            block = self._ignore_comments(block)

            tokens = b"".join(block.split())
            for token in tokens:
                if token not in (48, 49):
                    msg = b"Invalid token for this mode: %s" % bytes([token])
                    raise ValueError(msg)
            data = (data + tokens)[:total_bytes]
        invert = bytes.maketrans(b"01", b"\xFF\x00")
        return data.translate(invert)
