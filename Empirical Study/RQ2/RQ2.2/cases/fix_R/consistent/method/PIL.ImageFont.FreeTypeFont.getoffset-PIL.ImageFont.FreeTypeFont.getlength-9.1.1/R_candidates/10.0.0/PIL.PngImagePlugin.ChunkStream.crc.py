    def crc(self, cid, data):
        """Read and verify checksum"""

        # Skip CRC checks for ancillary chunks if allowed to load truncated
        # images
        # 5th byte of first char is 1 [specs, section 5.4]
        if ImageFile.LOAD_TRUNCATED_IMAGES and (cid[0] >> 5 & 1):
            self.crc_skip(cid, data)
            return

        try:
            crc1 = _crc32(data, _crc32(cid))
            crc2 = i32(self.fp.read(4))
            if crc1 != crc2:
                msg = f"broken PNG file (bad header checksum in {repr(cid)})"
                raise SyntaxError(msg)
        except struct.error as e:
            msg = f"broken PNG file (incomplete checksum in {repr(cid)})"
            raise SyntaxError(msg) from e
