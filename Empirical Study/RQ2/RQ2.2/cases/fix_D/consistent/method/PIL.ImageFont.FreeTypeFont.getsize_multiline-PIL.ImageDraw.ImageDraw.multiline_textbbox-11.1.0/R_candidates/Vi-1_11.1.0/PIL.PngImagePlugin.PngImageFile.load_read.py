    def load_read(self, read_bytes: int) -> bytes:
        """internal: read more image data"""

        assert self.png is not None
        while self.__idat == 0:
            # end of chunk, skip forward to next one

            self.fp.read(4)  # CRC

            cid, pos, length = self.png.read()

            if cid not in [b"IDAT", b"DDAT", b"fdAT"]:
                self.png.push(cid, pos, length)
                return b""

            if cid == b"fdAT":
                try:
                    self.png.call(cid, pos, length)
                except EOFError:
                    pass
                self.__idat = length - 4  # sequence_num has already been read
            else:
                self.__idat = length  # empty chunks are allowed

        # read more data from this chunk
        if read_bytes <= 0:
            read_bytes = self.__idat
        else:
            read_bytes = min(read_bytes, self.__idat)

        self.__idat = self.__idat - read_bytes

        return self.fp.read(read_bytes)
