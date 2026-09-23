    def call(self, cid: bytes, pos: int, length: int) -> bytes:
        """Call the appropriate chunk handler"""

        logger.debug("STREAM %r %s %s", cid, pos, length)
        return getattr(self, f"chunk_{cid.decode('ascii')}")(pos, length)
