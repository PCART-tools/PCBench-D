    def verify(self, endchunk: bytes = b"IEND") -> list[bytes]:
        # Simple approach; just calculate checksum for all remaining
        # blocks.  Must be called directly after open.

        cids = []

        while True:
            try:
                cid, pos, length = self.read()
            except struct.error as e:
                msg = "truncated PNG file"
                raise OSError(msg) from e

            if cid == endchunk:
                break
            self.crc(cid, ImageFile._safe_read(self.fp, length))
            cids.append(cid)

        return cids
