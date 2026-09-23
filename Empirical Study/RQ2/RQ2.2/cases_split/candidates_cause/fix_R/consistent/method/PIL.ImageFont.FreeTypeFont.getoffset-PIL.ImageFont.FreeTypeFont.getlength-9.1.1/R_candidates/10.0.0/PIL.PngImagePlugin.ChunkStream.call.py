    def call(self, cid, pos, length):
        """Call the appropriate chunk handler"""

        logger.debug("STREAM %r %s %s", cid, pos, length)
        return getattr(self, "chunk_" + cid.decode("ascii"))(pos, length)
