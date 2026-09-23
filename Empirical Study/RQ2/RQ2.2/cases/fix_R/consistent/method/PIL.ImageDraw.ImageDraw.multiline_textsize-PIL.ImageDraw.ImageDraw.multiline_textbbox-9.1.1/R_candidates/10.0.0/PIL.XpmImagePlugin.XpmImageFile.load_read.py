    def load_read(self, bytes):
        #
        # load all image data in one chunk

        xsize, ysize = self.size

        s = [None] * ysize

        for i in range(ysize):
            s[i] = self.fp.readline()[1 : xsize + 1].ljust(xsize)

        return b"".join(s)
