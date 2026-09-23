    def verify(self):
        """Verify PNG file"""

        if self.fp is None:
            msg = "verify must be called directly after open"
            raise RuntimeError(msg)

        # back up to beginning of IDAT block
        self.fp.seek(self.tile[0][2] - 8)

        self.png.verify()
        self.png.close()

        if self._exclusive_fp:
            self.fp.close()
        self.fp = None
