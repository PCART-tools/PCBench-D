    def add(self, cid: bytes, data: bytes, after_idat: bool = False) -> None:
        """Appends an arbitrary chunk. Use with caution.

        :param cid: a byte string, 4 bytes long.
        :param data: a byte string of the encoded data
        :param after_idat: for use with private chunks. Whether the chunk
                           should be written after IDAT

        """

        self.chunks.append((cid, data, after_idat))
