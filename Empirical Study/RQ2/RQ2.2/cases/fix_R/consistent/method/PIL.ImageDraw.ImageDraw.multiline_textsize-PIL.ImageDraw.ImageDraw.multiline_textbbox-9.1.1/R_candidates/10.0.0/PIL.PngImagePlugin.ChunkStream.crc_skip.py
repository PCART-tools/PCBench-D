    def crc_skip(self, cid, data):
        """Read checksum"""

        self.fp.read(4)
