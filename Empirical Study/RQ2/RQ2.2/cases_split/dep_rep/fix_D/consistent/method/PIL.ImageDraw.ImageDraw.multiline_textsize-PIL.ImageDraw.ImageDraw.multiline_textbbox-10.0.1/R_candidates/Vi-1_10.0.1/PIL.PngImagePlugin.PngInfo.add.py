    def add(self, cid, data, after_idat=False):
        """Appends an arbitrary chunk. Use with caution.

        :param cid: a byte string, 4 bytes long.
        :param data: a byte string of the encoded data
        :param after_idat: for use with private chunks. Whether the chunk
                           should be written after IDAT

        """

        chunk = [cid, data]
        if after_idat:
            chunk.append(True)
        self.chunks.append(tuple(chunk))
