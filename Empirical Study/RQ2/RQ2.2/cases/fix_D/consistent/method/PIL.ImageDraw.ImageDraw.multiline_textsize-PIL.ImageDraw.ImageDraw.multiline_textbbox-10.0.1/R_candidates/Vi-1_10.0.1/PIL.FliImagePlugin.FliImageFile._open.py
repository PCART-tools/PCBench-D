    def _open(self):
        # HEAD
        s = self.fp.read(128)
        if not (_accept(s) and s[20:22] == b"\x00\x00"):
            msg = "not an FLI/FLC file"
            raise SyntaxError(msg)

        # frames
        self.n_frames = i16(s, 6)
        self.is_animated = self.n_frames > 1

        # image characteristics
        self.mode = "P"
        self._size = i16(s, 8), i16(s, 10)

        # animation speed
        duration = i32(s, 16)
        magic = i16(s, 4)
        if magic == 0xAF11:
            duration = (duration * 1000) // 70
        self.info["duration"] = duration

        # look for palette
        palette = [(a, a, a) for a in range(256)]

        s = self.fp.read(16)

        self.__offset = 128

        if i16(s, 4) == 0xF100:
            # prefix chunk; ignore it
            self.__offset = self.__offset + i32(s)
            s = self.fp.read(16)

        if i16(s, 4) == 0xF1FA:
            # look for palette chunk
            number_of_subchunks = i16(s, 6)
            chunk_size = None
            for _ in range(number_of_subchunks):
                if chunk_size is not None:
                    self.fp.seek(chunk_size - 6, os.SEEK_CUR)
                s = self.fp.read(6)
                chunk_type = i16(s, 4)
                if chunk_type in (4, 11):
                    self._palette(palette, 2 if chunk_type == 11 else 0)
                    break
                chunk_size = i32(s)
                if not chunk_size:
                    break

        palette = [o8(r) + o8(g) + o8(b) for (r, g, b) in palette]
        self.palette = ImagePalette.raw("RGB", b"".join(palette))

        # set things up to decode first frame
        self.__frame = -1
        self._fp = self.fp
        self.__rewind = self.fp.tell()
        self.seek(0)
