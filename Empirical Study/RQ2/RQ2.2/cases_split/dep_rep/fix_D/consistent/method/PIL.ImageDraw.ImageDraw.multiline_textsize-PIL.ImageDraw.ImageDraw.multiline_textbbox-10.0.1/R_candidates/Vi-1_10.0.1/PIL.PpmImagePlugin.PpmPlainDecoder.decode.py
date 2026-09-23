    def decode(self, buffer):
        self._comment_spans = False
        if self.mode == "1":
            data = self._decode_bitonal()
            rawmode = "1;8"
        else:
            maxval = self.args[-1]
            data = self._decode_blocks(maxval)
            rawmode = "I;32" if self.mode == "I" else self.mode
        self.set_as_raw(bytes(data), rawmode)
        return -1, 0
