    def _open(self):
        self._mode = "P"

        # read header fields
        header = self.fp.read(32 + 24 + 32 + 12)
        self._size = i32(header, 32), i32(header, 36)
        Image._decompression_bomb_check(self.size)

        # load pixel data
        offset = i32(header, 40)
        self.fp.seek(offset)

        # strings are null-terminated
        self.info["name"] = header[:32].split(b"\0", 1)[0]
        next_name = header[56 : 56 + 32].split(b"\0", 1)[0]
        if next_name:
            self.info["next_name"] = next_name
