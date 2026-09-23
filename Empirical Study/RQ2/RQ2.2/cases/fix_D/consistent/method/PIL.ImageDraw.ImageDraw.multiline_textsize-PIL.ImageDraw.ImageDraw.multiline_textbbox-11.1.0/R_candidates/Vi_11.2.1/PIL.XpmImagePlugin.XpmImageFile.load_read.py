    def load_read(self, read_bytes: int) -> bytes:
        #
        # load all image data in one chunk

        xsize, ysize = self.size

        s = [self.fp.readline()[1 : xsize + 1].ljust(xsize) for i in range(ysize)]

        return b"".join(s)
