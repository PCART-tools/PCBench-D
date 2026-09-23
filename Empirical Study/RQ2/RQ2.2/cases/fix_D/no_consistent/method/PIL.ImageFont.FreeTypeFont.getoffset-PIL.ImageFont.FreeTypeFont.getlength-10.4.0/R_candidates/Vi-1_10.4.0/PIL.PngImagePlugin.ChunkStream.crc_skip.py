    def crc_skip(self, cid: bytes, data: bytes) -> None:
        """Read checksum"""

        assert self.fp is not None
        self.fp.read(4)
