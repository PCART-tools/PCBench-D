    def decode(self, buffer):
        rawmode, stride, orientation = self.args
        pagesize = self.state.xsize * self.state.ysize
        zsize = len(self.mode)
        self.fd.seek(512)

        for band in range(zsize):
            channel = Image.new("L", (self.state.xsize, self.state.ysize))
            channel.frombytes(
                self.fd.read(2 * pagesize), "raw", "L;16B", stride, orientation
            )
            self.im.putband(channel.im, band)

        return -1, 0
